from django.contrib import admin
from .models import Note, Review

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin interface for Note model."""
    list_display = ['title', 'branch', 'year', 'subject', 'uploader', 'upload_date', 'download_count']
    list_filter = ['branch', 'year', 'upload_date']
    search_fields = ['title', 'description', 'subject', 'uploader__username']
    readonly_fields = ['upload_date', 'download_count']
    date_hierarchy = 'upload_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review model."""
    list_display = ['note', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['note__title', 'user__username', 'comment']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
