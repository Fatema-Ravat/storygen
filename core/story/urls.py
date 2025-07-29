""" Story app urls"""

from django.urls import path, include

urlpatterns = [
    path('api/', include('story.api.urls')),
]
