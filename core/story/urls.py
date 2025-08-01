""" Story app urls"""

from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/', include('story.api.urls')),
]
