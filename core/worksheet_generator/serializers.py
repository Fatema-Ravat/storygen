from .models import Worksheet, WorksheetImage
from rest_framework import serializers

class WorksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worksheet
        fields = "__all__"
        read_only_fields = ("id","pdf_file","created_at","user",)

class WorksheetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksheetImage
        fields = "__all__"