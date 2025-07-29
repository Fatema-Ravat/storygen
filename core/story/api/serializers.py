""" Serializer for story generation """
from rest_framework import serializers
from story.models import Story

class StoryRequestSerializer(serializers.Serializer):
    theme = serializers.CharField(max_length=100)
    characters = serializers.CharField(max_length = 200)
    moral = serializers.CharField(max_length = 200)

class StoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id','theme','characters','moral','content','created_at']