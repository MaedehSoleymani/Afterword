from django.db import models
from accounts.models import C_User
from django.utils import timezone

class Contact(models.Model):
    user=models.ForeignKey(C_User, on_delete=models.CASCADE, null=False)
    name= models.CharField(null=True, blank=True)
    email= models.EmailField(unique=True, null=False, blank=False)
    created_date= models.DateTimeField(auto_now_add=True)

class Letter(models.Model):

    STATUS_NOT_SCHEDULED = 'not_scheduled'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_SENT = 'sent'
    STATUS_FAILED= 'failed'
    STATUS_INACTIVITY_TRIGGERED = 'inactivity_triggered'

    STATUS_CHOICES = [
        (STATUS_NOT_SCHEDULED, 'Not Scheduled'),
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_SENT, 'Sent'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_INACTIVITY_TRIGGERED, 'Waiting for Inactivity Trigger')
    ]
    
    author= models.ForeignKey(C_User, on_delete=models.CASCADE, null=False)
    receiver= models.EmailField(null=False)
    subject= models.CharField(max_length=255, null=False)
    message= models.TextField(null=False)
    attachment = models.FileField(
        upload_to='message_attachments/%Y/%m/%d/',
        blank=True,null=True,
        help_text='Optional file attachment (PDF, DOC, images, etc.)')
    created_date= models.DateTimeField(auto_now_add=True, null=False)
    scheduled_date= models.DateTimeField(blank=True, null=True)
    sent_date= models.DateTimeField(blank=True, null=True)
    status= models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_SCHEDULED,
        null=False)
    send_on_inactivity = models.BooleanField(default=False, null=False, blank=False)
    inactivity_days = models.IntegerField(default=7, help_text="Days of inactivity before sending", null=True, blank=True)
    inactivity_triggered_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.subject