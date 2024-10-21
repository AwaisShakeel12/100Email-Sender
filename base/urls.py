from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('getnumber', views.get_number, name='get_number'),
    path('withcsv', views.withcsv, name='withcsv'),
    path('withexcel', views.withexcel, name='withexcel'),
    path('create_inputs/<int:n>/', views.create_inputs, name='create_inputs'),
]