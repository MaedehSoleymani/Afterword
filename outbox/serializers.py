from rest_framework import serializers
from .models import Letter

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ['id', 'subject', 'receiver', 'message', 'status', 'scheduled_date']
        read_only_fields = ['id', 'status']