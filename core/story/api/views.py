"""Views for story APIs"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from story.models import Story,StoryRevision
from .serializers import StoryRequestSerializer,StoryResponseSerializer,StoryRevisionSerializer,StoryReviseRequestSerializer
from story.utils.generator import generate_story_with_huggingface,generate_revise_story_with_huggingface

from django.shortcuts import get_object_or_404

class StoryGeneratorView(APIView):
    """ view to generate the story """

    def get(self,request):
        pass

    def post(self,request):
        serializer = StoryRequestSerializer(data=request.data)
        if serializer.is_valid():
            theme = serializer.validated_data['theme']
            characters = serializer.validated_data['characters']
            moral = serializer.validated_data['moral']

            print("Making call now...")
            story_text = generate_story_with_huggingface(theme,characters,moral)

            story_obj = Story.objects.create(theme=theme,characters=characters,
                                             moral=moral,content=story_text)
            response_serializer = StoryResponseSerializer(story_obj)
            return Response(response_serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StoryReviseView(APIView):
    """ view to update the story by giving further instruction to ai """

    def get(self,request,id):
        """ get all the revisions of the story """
        revisions = StoryRevision.objects.filter(story__id = id).order_by('created_at')
        serializer = StoryRevisionSerializer(revisions, many=True)
        return Response(serializer.data)

    def post(self,request,id):
        """ create the next revision for story based on given instruction """
        story_obj = get_object_or_404(Story,id=id)
        serializer = StoryReviseRequestSerializer(data=request.data)
        if serializer.is_valid():
            original_story = story_obj.content
            instruction = serializer.validated_data['instruction']

            print("Making revise call now...")
            revise_story_text = generate_revise_story_with_huggingface(original_story,instruction)

            revise_story_obj = StoryRevision.objects.create(story=story_obj,instruction=instruction,
                                                            revised_content = revise_story_text)
            response_serializer = StoryRevisionSerializer(revise_story_obj)
            return Response(response_serializer.data)

