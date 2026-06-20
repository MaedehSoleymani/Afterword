from django.contrib import admin
from .models import Letter

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'receiver', 'subject', 'message', 'status', 'created_date', 'scheduled_date']
    list_filter = ['status', 'created_date', 'author']
    search_fields = ['author', 'subject', 'receiver', 'message']
    list_editable = ['status']
    readonly_fields = ['created_date']
    list_per_page = 20
