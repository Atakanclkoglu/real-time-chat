from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework.permissions import AllowAny

# Create your views here.

from rest_framework.permissions import AllowAny

class ChatMessageListView(APIView):
    permission_classes = [AllowAny]  # Token gerektirmesin

    def get(self, request):
        room = request.GET.get('room')
        if not room:
            return Response({"error":"room parametresi gerekli"}, status=status.HTTP_400_BAD_REQUEST)

        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



