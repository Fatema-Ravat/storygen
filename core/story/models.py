""" Model for Story """
from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    """ Story model """

    theme = models.CharField(max_length=100)
    characters = models.CharField(max_length=200)
    moral = models.CharField(max_length=200)
    content = models.TextField(default="Once upon a time...")
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='stories')

    def __str__(self):
        return f"{self.theme}--{self.characters}--{self.moral}"

class StoryRevision(models.Model):
    """ Model for all the revisions of a story"""

    story = models.ForeignKey(to=Story,on_delete=models.CASCADE,related_name="revisions")
    instruction = models.CharField(max_length=200)
    revised_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    revision_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"Revision of {self.story.id}, created at {self.created_at}"
    
def story_image_upload_path(instance, filename):
    return f"story_images/story_{instance.story.id}/{filename}"

class StoryImage(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="images")
    prompt = models.TextField()
    image = models.ImageField(upload_to=story_image_upload_path)
    style = models.CharField(max_length=50, default="default")  # e.g., cartoon, realistic, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Story #{self.story.id} – {self.prompt[:30]}..."
