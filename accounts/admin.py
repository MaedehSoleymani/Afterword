from django.contrib import admin

# admin.py
class C_UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_author', 'is_staff']
    list_filter = ['is_author', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_author', 'is_staff', 'is_superuser')}),
    )