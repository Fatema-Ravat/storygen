""" API urls """
from django.urls import path
from .views import (StoryGeneratorView,StoryReviseView,
                    ApplyStoryRevisionView,StoryDetailView,StoryListView)

urlpatterns = [
    path('generate/', StoryGeneratorView.as_view(), name='generate_story'),
    path('stories/', StoryListView.as_view(),name='list_story'),
    path('story/<int:id>/', StoryDetailView.as_view(), name='detail_story'),
    path('story/<int:id>/revise/',StoryReviseView.as_view(),name='revise_story'),
    path('revisions/<int:revision_id>/apply/',ApplyStoryRevisionView.as_view(),name='apply_revision'),
]
