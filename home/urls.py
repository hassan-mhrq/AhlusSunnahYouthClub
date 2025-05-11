from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    
    path("", views.index, name = 'index'),
    path("homepage/", views.homepage, name = 'homepage'),
    path("base/", views.base, name = 'base'),
    path("quran/", views.quran, name = 'quran'),
    path("hadith/", views.hadith, name = 'hadith'),
    path("about/", views.about, name = 'about'),
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_view, name = 'login'),
    path("logout/", views.logout_view, name = 'logout'),
    path("contact", views.contact, name = 'contact'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('query/', views.query_view, name='query'),
    # path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    # path('reset-password/', views.reset_password_view, name='reset_password'),
]
