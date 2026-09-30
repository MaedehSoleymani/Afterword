from django.shortcuts import render
from rest_framework import status
import rest_framework.views import APIView
from rest_framework.response import Response
from API_app.serializers import LetterModelSerializer, ContactModelSerializer
from outbox.model import Letter, Contact

class MessageListView(APIView):
    def get(self, request):
        messages= Letter.objects.filter(author=request.user)
        serializer=LetterModelSerializer(messages, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)