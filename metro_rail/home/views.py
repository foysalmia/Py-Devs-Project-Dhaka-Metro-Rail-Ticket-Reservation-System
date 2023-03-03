from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'home/index.html')

def sign_in(request):
    return render(request,'home/signin.html')

def sign_up(request):
    return render(request,'home/signup.html')

def profile(request):
    return render(request,"home/userprofile.html")
