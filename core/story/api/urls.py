""" API urls """
from django.urls import path
from .views import StoryGeneratorView,StoryReviseView,ApplyStoryRevisionView

urlpatterns = [
    path('generate/', StoryGeneratorView.as_view(), name='generate-story'),
    path('<int:id>/revise/',StoryReviseView.as_view(),name='revise_story'),
    path('<int:revision_id>/apply/',ApplyStoryRevisionView.as_view(),name='apply_revision'),
]
