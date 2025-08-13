from django.shortcuts import render
from .models import WorksheetImage,Worksheet

from shared.utils.generator import generate_worksheet_content

from .serializers import WorksheetSerializer,WorksheetImageSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class WorksheetGeneratorView(viewsets.ModelViewSet):
    queryset = Worksheet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = WorksheetSerializer

    def get_queryset(self):
        return Worksheet.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def generate(self, request):
        data = request.data
        ai_result = generate_worksheet_content(
            subject=data.get("subject"),
            grade=data.get("grade"),
            worksheet_type=data.get("worksheet_type"),
            topic=data.get("topic"),
            num_questions=data.get("num_questions", 10)
        )
        if ai_result.get("error"):

            return Response(ai_result, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ai_result,status=status.HTTP_200_OK)

    


