from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),
    path('result/<poll_id>/', views.result, name='result'),
    path('vote/<poll_id>/', views.vote, name='vote'),
    path('delete/<poll_id>/', views.delete, name='delete'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

]
