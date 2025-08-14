from django.shortcuts import render
from .models import WorksheetImage,Worksheet

from shared.utils.generator import generate_worksheet_content
from shared.utils.pdf_generator import save_pdf_to_model,generate_pdf

from .serializers import WorksheetSerializer,WorksheetImageSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

class WorksheetGeneratorView(viewsets.ModelViewSet):
    queryset = Worksheet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = WorksheetSerializer

    def get_queryset(self):
        return Worksheet.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'POST' not allowed. Use generate/ method to create worksheet"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=["post"])
    def generate(self, request):
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Step 1: Generate worksheet content using AI
        ai_result = generate_worksheet_content(
            subject=data.get("subject"),
            grade=data.get("grade"),
            worksheet_type=data.get("worksheet_type"),
            topic=data.get("topic"),
            num_questions=data.get("num_questions", 10)
        )
        if ai_result.get("error"):
            return Response(ai_result, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 2: Save worksheet in DB
        worksheet = Worksheet.objects.create(
            user = request.user,
            title=data.get("title"),
            subject=data.get("subject"),
            grade=data.get("grade"),
            worksheet_type=data.get("worksheet_type"),            
            content=ai_result.get("content")
        )

        # Step 3: Serialize and return
        serializer = WorksheetSerializer(worksheet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def generate_pdf(self, request, pk=None):
        worksheet = self.get_object()

        # Prepare content list for PDF
        content_list = []
        for q in worksheet.content.get("questions", []):
            content_list.append(f"Q: {q}")
        content_list.append("\nAnswers:")
        for ans in worksheet.content.get("answers", []):
            content_list.append(f"- {ans}")

        
        filename = f"{worksheet.title}_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_file = generate_pdf(worksheet.title, content_list, output_filename=filename)

        return FileResponse(
        pdf_file,
        as_attachment=True,
        filename=f"{worksheet.title}.pdf",
        content_type='application/pdf'
        )
    
    


