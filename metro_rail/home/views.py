from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
# Create your views here.


def home(request):
    data={
        'title' : 'base'
    }
    return render(request, 'home/home.html', data)

def index(request):
    data = {
        'title' : 'Welcome',
    }
    return render(request,'home/index.html',data)

def sign_in(request):
    data = {
        'title' : 'Sign In',
    }
    if request.method == 'GET':
        email = request.GET.get('email')
        data = {
            'email' : email,
        }
    return render(request,'home/signin.html',data)

def sign_up(request):
    data = {
        'title' : 'Sign Up',
    }
    try:
        if request.method == "POST":
            fast_name = request.POST.get('fast_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = int(request.POST.get('phone'))
            password = request.POST.get('password')
            conf_pass = request.POST.get('conf_password')
            data = {
                'fast_name' : fast_name,
                'last_name' : last_name,
                'email' : email,
                'phone' : phone,
                'password' : password,
                'conf_password' : conf_pass,
            }
            url = '/signin/?email={}'.format(email)
            return HttpResponseRedirect(url)
    except:
        pass
    
    return render(request,'home/signup.html',data)



def about_us(request):
    return render(request, 'about_us/about_us.html')

def contact_us(request):
    return render(request, 'contact_us/contact_us.html')
