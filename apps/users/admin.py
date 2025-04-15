from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for the User model.
    """
    list_display = ('username', 'email', 'organization', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

admin.site.register(User, UserAdmin)