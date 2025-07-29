""" API urls """
from django.urls import path
from .views import StoryGeneratorView

urlpatterns = [
    path('generate/', StoryGeneratorView.as_view(), name='generate-story'),
]
