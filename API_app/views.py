from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from API_app.serializers import LetterModelSerializer, ContactModelSerializer
from outbox.models import Letter, Contact
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class MessageListView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages=Letter.objects.filter(author=request.user)
        serializer=LetterModelSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)