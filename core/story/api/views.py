"""Views for story APIs"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from story.models import Story
from .serializers import StoryRequestSerializer,StoryResponseSerializer
from story.utils.generator import generate_story_with_huggingface

class StoryGeneratorView(APIView):
    """ view to generate the story """

    def post(self,request):
        serializer = StoryRequestSerializer(data=request.data)
        if serializer.is_valid():
            theme = serializer.validated_data['theme']
            characters = serializer.validated_data['characters']
            moral = serializer.validated_data['moral']

            print("Making call now...")
            story_text = generate_story_with_huggingface(theme,characters,moral)

            story_obj = Story.objects.create(theme=theme,characters=characters,moral=moral,content=story_text)
            response_serializer = StoryResponseSerializer(story_obj)
            return Response(response_serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

