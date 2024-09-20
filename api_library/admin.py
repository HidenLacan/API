from django.contrib import admin
from .models import Author, Book
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

# Get the custom User model
User = get_user_model()



try:
    user = User.objects.create_user(username='adminfantasma2', email='admin@example.com', password='helo')
except IntegrityError:
    print("User already exists!")
# Register the custom User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active','is_admin')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


# Customize Author admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

# Customize Book admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    search_fields = ('title', 'author__name')
    list_filter = ('pub_date', 'author')
