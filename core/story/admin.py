from django.contrib import admin

from story.models import Story,StoryRevision
# Register your models here.

admin.site.register(Story)
admin.site.register(StoryRevision)
