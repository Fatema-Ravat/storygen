from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login_view(request):
    return render(request,'login.html')

def generate_story(request):
    return render(request,'generate.html')

def story_detail(request,story_id):
    return render(request,'story_detail.html',{'story_id':story_id})

def revise_story(request,story_id):
    return render(request,'revise.html',{'story_id':story_id})

def list_revisions(request,story_id):
    return render(request,'revisions.html',{'story_id':story_id})

def illustrate_story(request,story_id):
    return render(request,'illustrate.html',{'story_id':story_id})

def home(request):
    return render(request,'home.html')

def register(request):
    return render(request,'register.html')

def mystories(request):
    return render(request,'mystories.html')

def detail_worksheet(request,worksheet_id):
    return render(request,'detail_worksheet.html',{'worksheet_id':worksheet_id})

def generate_worksheet(request):
    return render(request,'generate_worksheet.html')

def list_worksheet(request):
    return render(request,'list_worksheet.html')