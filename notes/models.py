from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

class Note(models.Model):
    """Model representing a student note/document."""
    
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('EEE', 'Electrical & Electronics'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('IT', 'Information Technology'),
    ]
    
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    subject = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='notes/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_notes')
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    is_premium_preview = models.BooleanField(default=False, help_text="If True, this note is premium preview only and cannot be downloaded.")
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        """Calculate average rating from all reviews."""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @property
    def file_size_mb(self):
        """Return file size in MB."""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0


class Review(models.Model):
    """Model representing a review/rating for a note."""
    
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['note', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.note.title} ({self.rating}/5)"
