from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import C_User

@admin.register(C_User)
class C_UserAdmin(UserAdmin):
    list_display = ('email', 'is_author', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_author', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_author')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_author', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )