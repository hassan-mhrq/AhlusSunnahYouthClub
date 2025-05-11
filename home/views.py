from django.shortcuts import render, HttpResponse , redirect
from django.urls import reverse
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm
import random
from django.core.mail import send_mail
from django.utils import timezone
from .models import PasswordResetOTP


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
    
    email_verified = request.session.get('signup_email_verified', False)
    otp_verified = request.session.get('signup_otp_verified', False)
    verified_email = request.session.get('signup_verified_email', '')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'send_otp':
            email = request.POST.get('email')
            otp = str(random.randint(100000, 999999))
            request.session['signup_otp'] = otp
            request.session['signup_verified_email'] = email
            request.session['signup_email_verified'] = True

            send_mail(
                'Your OTP for Signup',
                f'Your OTP is: {otp}',
                'smarttvofkitchen@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your email.')
            return redirect('signup')

        elif action == 'verify_otp':
            entered_otp = request.POST.get('otp')
            if entered_otp == request.session.get('signup_otp'):
                request.session['signup_otp_verified'] = True
                messages.success(request, 'Email verified successfully.')
            else:
                messages.error(request, 'Incorrect OTP. Please try again.')
            return redirect('signup')

        elif action == 'submit_signup' and email_verified and otp_verified:
            username = request.POST.get('username')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            confirm_password = request.POST.get('password_confirm')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('signup')

            email = verified_email
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('signup')

            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
            )
            messages.success(request, 'Account created successfully! You can now log in.')
            request.session.flush()
            return redirect('login')

    return render(request, 'signup.html', {
        'email_verified': email_verified,
        'otp_verified': otp_verified,
        'verified_email': verified_email
    })


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
    email_verified = request.session.get('email_verified', False)
    otp_verified = request.session.get('otp_verified', False)
    verified_email = request.session.get('verified_email', '')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'send_otp':
            email = request.POST.get('email')
            otp = str(random.randint(100000, 999999))

            request.session['otp'] = otp
            request.session['verified_email'] = email
            request.session['email_verified'] = True  # To show OTP input form

            send_mail(
                'Your AhlusSunnahYouthClub OTP',
                f'Your OTP is: {otp}',
                'smarttvofkitchen@gmail.com',  # Replace with your "from" email
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('contact')

        elif action == 'verify_otp':
            user_otp = request.POST.get('otp')
            if user_otp == request.session.get('otp'):
                request.session['otp_verified'] = True
                messages.success(request, 'Email verified successfully.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('contact')

        elif action == 'submit_form' and email_verified and otp_verified:
            # Process form data here
            name = request.POST.get('name')
            username = request.POST.get('username')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            comment = request.POST.get('comment')
            email = request.POST.get('email')

            # You can save this to a model, send an email, etc.
            messages.success(request, 'Thank you for contacting us!')
            # Optionally clear session
            request.session.flush()
            return redirect('contact')

    return render(request, 'contact.html', {
        'email_verified': email_verified,
        'otp_verified': otp_verified,
        'verified_email': verified_email
    })


def query_view(request):
    if request.method == "POST":
        hadees_number = request.POST.get("hadees_number")
        line_number = request.POST.get("line_number")
        query_text = request.POST.get("query_text")

        # You can save this data to a model here if needed
        # Example: Query.objects.create(...)

        messages.success(request, "Your query has been submitted successfully.")
        return redirect('query')  # This matches the name you’ll give in urls.py

    return render(request, 'query.html')  # This loads your query.html template






#Email verification, OTP , reset password


# def forgot_password_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         send_otp_email(email)
#         request.session['reset_email'] = email
#         return redirect('verify_otp')
#     return render(request, 'forgot_password.html')


# def send_otp_email(user_email):
#     otp = random.randint(100000, 999999)
#     expiry = timezone.now() + timezone.timedelta(minutes=10)

#     # Save OTP to DB (create PasswordResetOTP model if needed)
#     PasswordResetOTP.objects.update_or_create(
#         email=user_email,
#         defaults={'otp': otp, 'expires_at': expiry}
#     )

#     send_mail(
#         subject='Your Password Reset OTP',
#         message=f'Your OTP is {otp}. It will expire in 10 minutes.',
#         from_email='noreply@yourdomain.com',
#         recipient_list=[user_email]
#     )
    

# def verify_otp_view(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         email = request.session.get('reset_email')
#         record = PasswordResetOTP.objects.get(email=email)
#         if record.is_valid(entered_otp):
#             return redirect('reset_password')
#         else:
#             messages.error(request, 'Invalid or expired OTP')
#     return render(request, 'verify_otp.html')

def forgot_password_view(request):
    step = 'email'

    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                expiry = timezone.now() + timezone.timedelta(minutes=10)

                PasswordResetOTP.objects.update_or_create(
                    email=email,
                    defaults={'otp': otp, 'expires_at': expiry}
                )

                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is {otp}',
                    'smarttvofkitchen@gmail.com',
                    [email],
                )

                request.session['reset_email'] = email
                messages.info(request, 'OTP sent to your email.')
                step = 'otp'
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email.')

        elif 'otp' in request.POST:
            otp = request.POST.get('otp')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            email = request.session.get('reset_email')

            if not email:
                messages.error(request, 'Session expired. Try again.')
                return redirect('forgot_password')

            try:
                record = PasswordResetOTP.objects.get(email=email)
                if record.otp == otp and timezone.now() < record.expires_at:
                    if new_password != confirm_password:
                        messages.error(request, 'Passwords do not match.')
                        step = 'otp'
                    else:
                        user = User.objects.get(email=email)
                        user.set_password(new_password)
                        user.save()
                        record.delete()
                        messages.success(request, 'Password has been reset. You can now log in.')
                        return redirect('login')
                else:
                    messages.error(request, 'Invalid or expired OTP.')
                    step = 'otp'
            except PasswordResetOTP.DoesNotExist:
                messages.error(request, 'OTP not found. Try again.')
                step = 'email'
                
        elif 'otp' in request.POST or request.POST.get('action') == 'resend':
            email = request.session.get('reset_email')

            if not email:
                 messages.error(request, 'Session expired. Try again.')
                 return redirect('forgot_password')

            # Handle resend OTP
            if request.POST.get('action') == 'resend':
                otp = str(random.randint(100000, 999999))
                expiry = timezone.now() + timezone.timedelta(minutes=10)

                PasswordResetOTP.objects.update_or_create(
                    email=email,
                    defaults={'otp': otp, 'expires_at': expiry}
                )

                send_mail(
                    'Your New OTP for Password Reset',
                    f'Your new OTP is {otp}',
                    'noreply@yourdomain.com',
                    [email],
                )

                messages.info(request, 'A new OTP has been sent to your email.')
                step = 'otp'

    else:
        request.session.pop('reset_email', None)

    return render(request, 'forgot_password.html', {'step': step})