from django.shortcuts import render, HttpResponse , redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login as auth_login, logout


# Create your views here.

def index(request):
    return render(request,'index.html')


def base(request):
    return render(request,'base.html')


def homepage(request):
    return render(request,'homepage.html')


def quran(request):
    return render(request,'quran.html')


def hadith(request):
    return render(request,'hadith.html')


def about(request):
    return render(request,'about.html')


def login_view(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}! You have successfully logged in.")
            return redirect("/homepage")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    return render(request,'login.html')


def logout(request):
    return render(request,'index.html')


def contact(request):
    if request.method=="POST":
         name = request.POST.get('name')
         username = request.POST.get('username')
         email = request.POST.get('email')
         contact = request.POST.get('phone')
         address = request.POST.get('address')
         comment = request.POST.get('comment')
         contact_input = Contact(name=name, username= username, email=email, contact=contact, address=address, comment=comment , date=datetime.now())
         contact_input.save()
         messages.success(request, " ")
    
    return render(request,'contact.html')