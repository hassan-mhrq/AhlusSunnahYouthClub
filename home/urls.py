from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    
    path("", views.index, name = 'index'),
    path("homepage", views.homepage, name = 'homepage'),
    path("base", views.base, name = 'base'),
    path("quran", views.quran, name = 'quran'),
    path("hadith", views.hadith, name = 'hadith'),
    path("about", views.about, name = 'about'),
    path("login", views.login_view, name = 'login'),
    path("logout", views.logout, name = 'logout'),
    path("contact", views.contact, name = 'contact'),
] 
