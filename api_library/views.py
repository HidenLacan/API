from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from .models import Author, Book,Favorite
from .serializers import AuthorSerializer, BookSerializer, CustomUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from rest_framework import filters
from django.db.models import Q

from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

from .serializers import AuthorSerializer


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]  
    
    def get_permissions(self):
        # Allow GET requests without authentication
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [permission() for permission in self.permission_classes]
        # Require authentication for POST, PUT, and DELETE actions
        return [IsAuthenticated()]
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']

    def get_permissions(self):
        # Allow GET requests without authentication
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [permission() for permission in self.permission_classes]
        # Require authentication for POST, PUT, and DELETE actions
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Check if the request contains a list of books
        if isinstance(request.data, list):
            # If it's a list, handle bulk creation
            serializer = BookSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If it's a single book, handle it normally
            return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, serializer):
        serializer.save()

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        data = request.data
        serializer = CustomUserSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'detail': 'User registered successfully',
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"detail": "User with this email or username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # If the request is GET, render the registration HTML template
    return render(request, 'register.html')
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        if favorite.books.count() < 20:
            favorite.books.add(book)
            return Response({"detail": "Book added to favorites."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Maximum limit of 20 favorite books reached."}, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        favorite = Favorite.objects.get(user=request.user)
        favorite.books.remove(book)
        return Response({"detail": "Book removed from favorites."}, status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
    except Favorite.DoesNotExist:
        return Response({"detail": "Favorite list not found."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    try:
        favorite = Favorite.objects.get(user=request.user)
        books = favorite.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Favorite.DoesNotExist:
        return Response({"detail": "No favorite books found."}, status=status.HTTP_404_NOT_FOUND)

import numpy as np

def recommend_books_content_based(user):
    cache_key = f'recommendations_{user.id}'
    recommended_books = cache.get(cache_key)

    if not recommended_books:
        try:
            favorite = Favorite.objects.get(user=user)
            favorite_books = favorite.books.all()

            # Collect descriptions of all books except the ones in user's favorites
            all_books = Book.objects.exclude(id__in=favorite_books.values_list('id', flat=True))
            descriptions = list(all_books.values_list('description', flat=True))
            fav_descriptions = list(favorite_books.values_list('description', flat=True))

            # Combine all descriptions for TF-IDF Vectorization
            combined_descriptions = fav_descriptions + descriptions

            # TF-IDF Vectorization
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(combined_descriptions)

            # Compute cosine similarity between favorite books and all books
            cosine_similarities = cosine_similarity(tfidf_matrix[:len(fav_descriptions)], tfidf_matrix[len(fav_descriptions):])

            # Rank the books by similarity scores
            top_similar_books_indices = cosine_similarities.mean(axis=0).argsort()[::-1][:5]

            # Cast indices to Python integers and fetch the recommended books
            top_similar_books_indices = [int(index) for index in top_similar_books_indices]
            recommended_books = [all_books[index] for index in top_similar_books_indices]

            # Cache recommendations for future use
            cache.set(cache_key, recommended_books, timeout=60*60)

        except Favorite.DoesNotExist:
            # If no favorites exist, return an empty recommendation
            recommended_books = []

    return recommended_books


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    recommended_books = recommend_books_content_based(request.user)
    if recommended_books:
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({"detail": "No recommendations available."}, status=404)




    


