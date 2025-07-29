""" Model for Story """
from django.db import models

class Story(models.Model):
    """ Story model """

    theme = models.CharField(max_length=100)
    characters = models.CharField(max_length=200)
    moral = models.CharField(max_length=200)
    content = models.TextField(default="Once upon a time...")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.theme}--{self.characters}--{self.moral}"

