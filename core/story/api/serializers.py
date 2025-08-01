""" Serializer for story generation """
from rest_framework import serializers
from story.models import Story,StoryRevision

class StoryRequestSerializer(serializers.Serializer):
    theme = serializers.CharField(max_length=100)
    characters = serializers.CharField(max_length = 200)
    moral = serializers.CharField(max_length = 200)

class StoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__' #['id','theme','characters','moral','content','created_at']

class StoryReviseRequestSerializer(serializers.Serializer):
    instruction = serializers.CharField(max_length=300)

class StoryRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRevision
        fields = '__all__' #['id','story','instruction','revised_content','created_at','revision_applied']