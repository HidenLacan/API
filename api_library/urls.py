from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet,register,add_favorite, remove_favorite,get_favorites,get_recommendations
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),  
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('recommendations/', get_recommendations, name='get_recommendations'),
    path('books/<int:book_id>/add_favorite/', add_favorite, name='add_favorite'),
    path('books/<int:book_id>/remove_favorite/', remove_favorite, name='remove_favorite'),
    path('favorites/', get_favorites, name='get_favorites'),
]


