from rest_framework import serializers

class SentenceSerializer(serializers.Serializer):
    sentence1 = serializers.CharField(max_length=200)
    sentence2 = serializers.CharField(max_length=200)
