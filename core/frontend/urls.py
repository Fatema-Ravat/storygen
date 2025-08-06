from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view, name='login'),
    path('mystories/',views.mystories, name='mystories'),
    path('generate/',views.generate_story,name='generate'),
    path('story/<int:story_id>/',views.story_detail,name='story_detail'),
    path('story/<int:story_id>/revise/',views.revise_story,name='revise'),
    path('story/<int:story_id>/revisions/',views.list_revisions,name='revisions'),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
]