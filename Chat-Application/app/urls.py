from django.urls import path
from .views import *

urlpatterns = [
    path('', homePage, name='home'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('users/', usersPage, name='users'),
    path('chat/<str:username>/<str:other_username>', chatPage, name='chat'),
]