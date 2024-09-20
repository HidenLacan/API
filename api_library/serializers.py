from rest_framework import serializers
from .models import Book, Author

from api_library.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework import status


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
        #extra_kwargs = {
        #    'id': {'read_only': False, 'required': False},  # Allow the ID to be included in the request
        #}

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id','title', 'author', 'description', 'pub_date']

    def create(self, validated_data):
        # Extract the author data from the validated data
        author_data = validated_data.pop('author')
        
        # Get or create the Author instance from the provided data
        author, created = Author.objects.get_or_create(name=author_data['name'])
        
        # Create a new Book instance with the provided data and associated author
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        # Extract the author data
        author_data = validated_data.pop('author')
        
        # Get or create the Author instance
        author, created = Author.objects.get_or_create(name=author_data['name'])
        
        # Update the book's fields
        instance.author = author
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        
        instance.save()
        return instance




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures that the password is write-only
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hashes the password
        user.save()
        return user

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
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

