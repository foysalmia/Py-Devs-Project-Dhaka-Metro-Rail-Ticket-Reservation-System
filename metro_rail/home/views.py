from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
# from .forms import OrderForm, CreateUserForm
from .forms import CreateUserForm
#from home.models import Contacts


def index(request):
    data = {
        'title' : 'Welcome',
    }
    return render(request,'home/index.html',data)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('signin')

        context = {'form' : form}
        return render(request,'home/signup.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request , username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return render(request,'home/signin.html')

        context = {}
        return render(request,'home/signin.html',context)


@login_required(login_url='signin')
def home(request):
    data={
        'title' : 'base'
    }
    return render(request, 'home/home.html', data)


@login_required(login_url='signin')
def log_out(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def about_us(request):
    return render(request, 'about_us/about_us.html')


@login_required(login_url='signin')
def contact_us(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        print(name, email, content)

        if len(name)<3 or len(email)<6 or len(content)<4:
            messages.error(request, "Please fill the form correctly!")
        else:
            contact = Contact(name = name, email = email, content = content)
            contact.save()
            messages.success(request, "Your message has been sent successfully!")
    return render(request, 'contact_us/contact_us.html')
