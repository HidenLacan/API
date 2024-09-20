from django.contrib import admin
from .models import Author, Book
from django.contrib.auth import get_user_model

AUTH_USER_MODEL = 'api_library.User'
# Register the custom User model
User = get_user_model()
admin.site.register(User)

# Customize Author admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
# Customize Book admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'genre')
    search_fields = ('title', 'author__name', 'genre')
    list_filter = ('pub_date', 'genre')
