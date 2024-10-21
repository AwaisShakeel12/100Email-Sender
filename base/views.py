from django.shortcuts import redirect, render
from django.forms import Form, CharField
from .forms import NumberForm
from django.core.mail import send_mail, EmailMessage, get_connection
from django.conf import settings
import pandas as pd

from django.contrib.auth import login, logout, authenticate
from django.contrib import auth
from django.contrib import messages
from .models import *
from project.settings import get_email_settings



def home(request):
    return render(request, 'home.html')




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        re_enter_password = request.POST['password1']
        email = request.POST['email']
        app_password = request.POST['app_password']



        if password == re_enter_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exsist')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exsist')
                return redirect('register')
            else:
                
                user = User.objects.create_user(username=username, email=email, password=password,  app_password=app_password)
                user.save()

                user_login = auth.authenticate(username=username,password=password)
                auth.login(request, user_login)
                return redirect('get_number')
              
        else:

            messages.info(request, 'invalid data')
            return redirect('register')
    return render(request, 'register2.html')




def login(request):

    if request.user.is_authenticated:
        return redirect('get_number')
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('get_number')
        else:
            messages.info(request, 'username or password inccorect')

    return render(request, 'login.html')



def logout(request):
    auth.logout(request)
    return redirect('login')






def get_number(request):
 
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
  
            return redirect('create_inputs', n=n, )
    else:
        form = NumberForm()
    return render(request, 'new.html', {'form': form})



def create_inputs(request, n):


    if request.method == 'POST':

        user = request.user
        email_settings = get_email_settings(user)     
        input_value_list = []
        name = request.POST['name']
        message = request.POST['message']
        attachment = request.FILES.get('attachment')


        for i  in range(n):
            input_name = f'input_{i}'
            input_value = request.POST.get(input_name)
            input_value_list.append(input_value)

 

        email = EmailMessage(
            name,
            message,
            email_settings['EMAIL_HOST_USER'],
            to=input_value_list,
            connection=get_connection(
                username=email_settings['EMAIL_HOST_USER'],
                password=email_settings['EMAIL_HOST_PASSWORD'],
            )
        )
        if message:
            print('send')
        else:
            print('no msg enter')    
        email.content_subtype = 'html'

        if attachment:
            email.attach(
                filename=attachment.name,  
                content=attachment.read(),  
                mimetype=attachment.content_type 
                
            )
                
        else:
            print('no attachment')    
       
        email.send(fail_silently=False)
       

            

        context = {
            'input_value_list':input_value_list,
            'message': 'Inputs stored successfully',
           
                   
            }    
        return render(request, 'new.html', context)

    else:        
        input_fields = []
        for i in range(n):
            input_fields.append({'label': f'Input {i+1}', 'name': f'input_{i}'})



    return render(request, 'new.html', {'input_fields': input_fields})




def withcsv(request):

    if request.method == 'POST':

        mylist = []
        user = request.user
        email_settings = get_email_settings(user)     
        address = request.POST['address']
        column = request.POST['column']
        name = request.POST['name']
        message = request.POST['message']
        attachment = request.FILES.get('attachment')

        read = pd.read_csv(address)
        data = read[column]
        # print(a)
        
        for i in data:
            mylist.append(i)
        print(mylist) 


        email = EmailMessage(
            name,
            message,
            email_settings['EMAIL_HOST_USER'],
            to=mylist,
            connection=get_connection(
                username=email_settings['EMAIL_HOST_USER'],
                password=email_settings['EMAIL_HOST_PASSWORD'],
            )
        )
        email.content_subtype = 'html'
        if attachment:
            # email.attach(attachment.name, attachment.read(), attachment.content_type)
            email.attach(
                filename=attachment.name,  
                content=attachment.read(),  
                mimetype=attachment.content_type 
                
            )
                
        else:
            print('no attachment')    
       
        email.send(fail_silently=False)
       

    return render(request,'withcsv.html')




def withexcel(request):

    if request.method == 'POST':
        mylist = []
        user = request.user
        email_settings = get_email_settings(user)    
        address = request.POST['address']
        column = request.POST['column']
        name = request.POST['name']
        message = request.POST['message']
        attachment = request.FILES.get('attachment')

        read = pd.read_excel(address)
        data = read[column]
        # print(a)
        
        for i in data:
            mylist.append(i)
        print(mylist) 


        email = EmailMessage(
            name,
            message,
            email_settings['EMAIL_HOST_USER'],
            to=mylist,
            connection=get_connection(
                username=email_settings['EMAIL_HOST_USER'],
                password=email_settings['EMAIL_HOST_PASSWORD'],
            )
          
        )
        email.content_subtype = 'html'
        if attachment:
            email.attach(
                filename=attachment.name,  
                content=attachment.read(),  
                mimetype=attachment.content_type 
                
            )
                
        else:
            print('no attachment')    
       
        email.send(fail_silently=False)
       

    return render(request,'withExcel.html')


