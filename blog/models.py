from django.db import models
from accounts.models import C_User
from django.utils import timezone

class Post(models.Model):
        
    STATUS_DRAFT='draft'
    STATUS_SCHEDULED='scheduled'
    STATUS_PUBLISHED='published'

    STATUS_CHOICES=[
        (STATUS_DRAFT,'Draft'),
        (STATUS_SCHEDULED,'Scheduled'),
        (STATUS_PUBLISHED,'Published')]

    author=models.ForeignKey(C_User, on_delete=models.CASCADE, null=False)
    title=models.CharField(max_length=255, blank=True, null=True)
    content=models.TextField(blank=True, null=True)
    created_date=models.DateTimeField(auto_now_add=True, null=False)
    publish_date=models.DateTimeField(blank=True, null=True)
    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        null=False)
    img=models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        verbose_name='Post Image')