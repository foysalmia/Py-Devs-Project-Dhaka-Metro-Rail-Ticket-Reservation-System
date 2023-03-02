from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.
from .models import *
# from .forms import OrderForm, CreateUserForm
from .forms import CreateUserForm


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
    routes = Routes.objects.all()
    data={
        'routes' : routes
    }
    
    if request.method == 'POST':
        from_station = request.POST['from']
        to_station = request.POST['to']
        date = request.POST['date']
        seat = request.POST['seat']
        quantity = int(request.POST['quantity'])
        user = request.user.username

        #calculation distance
        from_station_no = 0
        to_station_no = 0
        for station in routes:
            if from_station == station.name:
                from_station_no = station.station_no
                # print(station.station_no)
            if to_station == station.name:
                to_station_no = station.station_no
            
            if from_station_no and to_station_no:
                break

        distance = abs(to_station_no - from_station_no)
        # print(distance)

        #calculating Cost
        total_cost = 0
        if seat=="AC":
            total_cost = quantity * 20 * distance
        elif seat == "Non AC":
            total_cost = quantity * 15 * distance
        else:
            total_cost = quantity * 10 * distance

        if total_cost / quantity < 20:
            total_cost = 20 * quantity

        print(total_cost)
        trip = Trips.objects.create(from_station=from_station,to_station=to_station,date=date,seat_type=seat,seat_quantity=quantity,passenger=user,cost=total_cost)
        trip.save()
        if trip:
            print(from_station,to_station,date,seat,quantity, user)

            return render(request,'book/book.html',{'trips':trip})
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
    return render(request, 'contact_us/contact_us.html')


@login_required(login_url='signin')
def booking(request):
    return render(request, 'book/book.html')
