from rest_framework import serializers
from outbox.models import Letter, Contact

class LetterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Letter
        fields= '__all__'

class ContactModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Contact
        fields= '__all__'