# myapp/serializers.py
from rest_framework import serializers

class TextGenerationSerializer(serializers.Serializer):
    text = serializers.CharField()
