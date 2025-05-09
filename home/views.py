from django.shortcuts import render, HttpResponse , redirect
from django.urls import reverse
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login as auth_login, logout as auth_logout
from .forms import SignUpForm


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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash the password
            user.save()
            auth_login(request, user)
            messages.success(request, 'Sign-up successful! You are now logged in.')
            return redirect('homepage')  # replace with your desired page
        else:
            messages.error(request, 'There was an error in your sign-up form.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user exists and the credentials are correct
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # print("Login successful for:", user.username)
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}! You have successfully logged in.")
            return redirect("homepage")  # Redirect to homepage or the page you want after login
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')  # Return to login page if credentials are wrong
    
    return render(request, 'login.html')  # If GET request, show login page


def logout_view(request):
    auth_logout(request)  # This logs the user out
    messages.success(request, "You have successfully logged out.")
    return redirect('index')  # Redirect to the index or homepage after logout


def contact(request):
    if request.method=="POST":
         name = request.POST.get('name')
         username = request.POST.get('username')
         email = request.POST.get('email')
         phone = request.POST.get('phone')
         address = request.POST.get('address')
         comment = request.POST.get('comment')
         contact_input = Contact(name=name, username= username, email=email, contact=phone, address=address, comment=comment , date=datetime.now())
         contact_input.save()
         
         messages.success(request, "Submitted successfully! We'll contact you shortly.")
         return redirect('contact')  # reload form and show success message
    
    return render(request,'contact.html')