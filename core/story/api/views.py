"""Views for story APIs"""
import os
from django.conf import settings
from django.core.files import File

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from story.models import Story,StoryRevision,StoryImage
from .serializers import (StoryRequestSerializer,StoryResponseSerializer,
                        StoryRevisionSerializer,StoryReviseRequestSerializer,
                        ApplyRevisionResponseSerializer,StoryImageResponseSerializer)

from story.utils.generator import (generate_story_with_huggingface,
                                   generate_revise_story_with_huggingface,
                                   generate_image_prompts_from_story)
from story.utils.image_generation import generate_image_from_prompt

from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema,OpenApiParameter

from story.utils.misc import can_user_generate


@extend_schema(
    request=StoryRequestSerializer,
    responses=StoryResponseSerializer
)
class StoryGeneratorView(APIView):
    """ view to generate the story """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = StoryRequestSerializer(data=request.data)
        if serializer.is_valid():
            theme = serializer.validated_data['theme']
            characters = serializer.validated_data['characters']
            moral = serializer.validated_data['moral']

            try:
                #checking the daily call limit for user
                user_id = request.user.id
                if not can_user_generate(user_id,daily_limit=3):
                    return Response({"error":"Daily Story Generate/Revise limit reached"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            except Exception as e:
                print(e) #to handle redis exception for now.

            print("Making call now...")
            try:
                story_text = generate_story_with_huggingface(theme,characters,moral)
                story_obj = Story.objects.create(theme=theme,characters=characters,
                                                moral=moral,content=story_text,user=request.user)
                response_serializer = StoryResponseSerializer(story_obj)
                return Response(response_serializer.data)
            except Exception as e:
                return Response({"error":str(e)},status=e.status)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=None,
    responses = StoryResponseSerializer
)
class StoryDetailView(APIView):
    """ detail view of story object """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,id):
        """ Get the detail of the given id """
        story_obj = get_object_or_404(Story,id=id)
        response_serializer = StoryResponseSerializer(story_obj)
        return Response(response_serializer.data)


@extend_schema(
    request=None,
    responses = StoryResponseSerializer
)
class StoryListView(APIView):
    """ detail view of story object """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        """ Get the list of all the stories by an user. """
        stories = Story.objects.filter(user=request.user).order_by('-created_at')
        response_serializer = StoryResponseSerializer(stories, many=True)
        return Response(response_serializer.data)
    

@extend_schema(
    request=StoryReviseRequestSerializer,
    responses=StoryRevisionSerializer
)
class StoryReviseView(APIView):
    """ view to update the story by giving further instruction to ai """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,id):
        """ get all the revisions of the story """
        revisions = StoryRevision.objects.filter(story__id = id,story__user=request.user).order_by('-created_at')
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

            try:
                revise_story_text = generate_revise_story_with_huggingface(original_story,instruction)

                revise_story_obj = StoryRevision.objects.create(story=story_obj,instruction=instruction,
                                                                revised_content = revise_story_text)
                response_serializer = StoryRevisionSerializer(revise_story_obj)
                return Response(response_serializer.data)
            except Exception as e:
                return Response({"error":str(e)},status=e.status)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

@extend_schema(
    request=None,
    responses=ApplyRevisionResponseSerializer
)
class ApplyStoryRevisionView(APIView):
    """ endpoint to apply a particular revision to the main story """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,revision_id):
        """make the revised_content of the revision main story content """
        revision_obj = StoryRevision.objects.select_related('story').filter(id=revision_id,story__user=request.user).first()
        if revision_obj is None:
            return Response(data = {"message":"REvison not found"},status=status.HTTP_400_BAD_REQUEST)
        revision_obj.story.content = revision_obj.revised_content
        revision_obj.story.save()

        revision_obj.revision_applied = True
        revision_obj.save()

        other_revisions = StoryRevision.objects.exclude(id=revision_obj.id).update(revision_applied=False)

        return Response(data={
                    "message":"Revision applied succesfully",
                    "updated_story":{
                        "id" : revision_obj.story.id,
                        "theme": revision_obj.story.theme,
                        "characters" : revision_obj.story.characters,
                        "moral": revision_obj.story.moral,
                        "content" : revision_obj.story.content,
                    }
        },status=status.HTTP_200_OK)

@extend_schema(
    parameters=[OpenApiParameter(name='style',required=False,type=str)],
    responses=StoryImageResponseSerializer    
)
class StoryIllustrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, story_id):
        story = Story.objects.filter(id=story_id, user=request.user).first()
        if not story:
            return Response({"error": "Story not found"}, status=404)

        style = request.data.get("style", "default")  # cartoon, realistic, etc.
        prompts = generate_image_prompts_from_story(story.content)

        saved_images = []
        for prompt in prompts:
            try:
                image_path = generate_image_from_prompt(prompt, style)
                if image_path:
                    abs_path = os.path.join(settings.MEDIA_ROOT,image_path)

                    with open(abs_path,'rb') as f:
                        image_obj = StoryImage.objects.create(
                            story=story,
                            prompt=prompt,
                            style=style                        
                        )
                        image_obj.image.save(os.path.basename(image_path),File(f),save=True)
                        saved_images.append(image_obj)
            except Exception as e:
                print("Image for prompt " + prompt + "gave errors: " + str(e))
                continue

        serializer = StoryImageResponseSerializer(saved_images,many=True)
        return Response(serializer.data)
