from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['session_id', 'disease', 'location', 'created_at', 'messages']

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    session_id = serializers.UUIDField(required=False, allow_null=True)

class ChatResponseSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    response = serializers.CharField()
    publications = serializers.ListField()
    trials = serializers.ListField()
    disease = serializers.CharField()
    location = serializers.CharField()
