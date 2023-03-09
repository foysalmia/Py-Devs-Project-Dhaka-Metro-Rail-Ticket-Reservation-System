from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from validate_email_address import validate_email
# Create your views here.
from .models import *
# from .forms import OrderForm, CreateUserForm
from .forms import CreateUserForm
# added by lukman
from metro_rail import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes # fource_tex not found
from .tokens import generate_token
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth.models import User



def index(request):
    data = {
        'title' : 'Welcome',
    }
    return render(request,'home/index.html',data)

def sign_up(request): # metro 2
    if request.user.is_authenticated:
        return redirect('home')
    else:
        # form = CreateUserForm()
        if request.method == 'POST':
            # form = CreateUserForm(request.POST)
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST['password1']
            print(password)
            

            myuser = User.objects.create(username=username,email=email,password=password)
            myuser.is_active = False
            myuser.save()
            print('no 1')

            if myuser.is_authenticated:     #form.is_valid()
                email = request.POST.get('email')
                if( validate_email(email,verify=True)):
                    print(request.POST.get('email'))

                    # wellcomr mail/ send succefully
                    sub = "Metro rail conformation"
                    msg = 'Well come to py devs Metro rail project\n Account has created for ' + username + ' by your email id'
                    to_email = [email]
                    send_mail(sub,msg,settings.EMAIL_HOST_USER,to_email,fail_silently=True)
                    # to_email = ['lukmanbinharun@gmail.com'] 

                    # Activation mail/ cann't send
                    current_side = get_current_site(request)
                    email_sub = 'Conform your account'
                    msg2 = render_to_string('email_conf.html',{
                        'name' : username,
                        'domain' : current_side.domain,
                        'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
                        'token': generate_token.make_token(myuser) 
                    })
                    print('no 2')
                    confarm_mail = EmailMessage(
                        email_sub,
                        msg2,
                        settings.EMAIL_HOST_USER,
                        [email] # resever
                        # ['lukmanbinharun@gmail.com']
                    )
                    confarm_mail.fail_silently = True
                    confarm_mail.send()

                    myuser.is_active = False
                    myuser.save()

                    messages.success(request, 'Account was created for ' + username +'\n. A massage has send to your mail')
                    return redirect('signin')
                else:
                    messages.warning(request,"Email doesn't exit")
        form = CreateUserForm()        
        context = {'form' : form}
        return render(request,'home/signup.html',context)
        
    


def activate(request,uidb64,token):
    try:
        # uid = fource_tex(urlsafe_base64_decode(uidb64))
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
        myuser.is_active = True
        myuser.save()
        print(uid,myuser)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    return HttpResponse("Your id has active")

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

