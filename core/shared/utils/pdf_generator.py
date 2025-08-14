from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from django.core.files.base import ContentFile
from django.utils import timezone

import os

def generate_pdf(title,content_list,output_filename=None):
    """ generates a pdf and returns BytesIO """

    buffer = BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4)
    width,height=A4

    p.setFont("Helvetica-Bold",18)
    p.drawCentredString(width / 2, height - 50, title)

    y = height - 100
    p.setFont("Helvetica", 12)
    for text in content_list:
        lines = text.split("\n")
        for line in lines:
            if y < 50:  # New page if too low
                p.showPage()
                p.setFont("Helvetica", 12)
                y = height - 50
            p.drawString(50, y, line)
            y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    if output_filename:
        return ContentFile(buffer.read(), name=output_filename)
    return buffer

def save_pdf_to_model(instance, title, content_list, field_name="pdf_file"):
    """    Generates and saves a PDF to a model instance's FileField.    """

    filename = f"{title}_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_file = generate_pdf(title, content_list, output_filename=filename)
    getattr(instance, field_name).save(filename, pdf_file, save=True)