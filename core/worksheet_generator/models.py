from django.db import models
from django.contrib.auth.models import User

class Worksheet(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Math'),
        ('science', 'Science'),
        ('english', 'English'),
        ('gk', 'General Knowledge'),
    ]
    TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('fill_blank', 'Fill in the Blank'),
        ('matching', 'Matching'),
        ('crossword', 'Crossword'),
        ('mixed', 'Mixed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="worksheets")
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    grade = models.CharField(max_length=50)
    worksheet_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    content = models.JSONField()  # Stores generated worksheet
    pdf_file = models.FileField(upload_to="worksheets/pdfs/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject})"

class WorksheetImage(models.Model):
    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE, related_name="wimages")
    image = models.ImageField(upload_to="worksheets/images/")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.worksheet.title}"

