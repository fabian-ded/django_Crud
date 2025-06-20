from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#el "UserCreationForm" es para crear un usuario y el "AuthenticationForm" es para cpprobar si el usuario existe
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError #esta biblioteca funciona para mostrar los errores mas detallados que hayamos tenido en la base de datos es decir si estaba haciendo una consulta o enviado datos a este
from django.http import HttpResponse
from .forms import TaskForm

# Create your views here.

def home(request):
    return render(request, 'home.html', {
    })
    
def signup(request):
    if request.method == 'GET':
        return render (request, 'signup.html', {'form': UserCreationForm }) #ese "UserCreationForm" es para crear un formulario que ya viene por defecto de django y utilizarlo en nuestra app
    else:
        if request.POST['password1'] == request.POST['password2']:#aqui estamos comparando las dos comtraseña que nos esta dando el usuario en el formulario de django
            try:#aqui se atrapa el error
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])#creamos una variable donde va atener la informacion del usuario que se esta creando, es decir que del espacio que dice "username" es el espacio que existe ya en la base de datos y ademas se le coloca otra vez "username" que esta se encuantra en la plantilla del html, al momento de que el espacio del 'username' le llegue un dato este dato lo enviara a la base de datos que esta como 'username'
                #User.objects.create_user: es para crear una tabla en la base de datos que sea para los usuarios que se estan creando en el formulario de django
                user.save()#aqui estamos diciendo que los datos creados se deben guardar
                login(request, user)#este login crea un tipo de autenticacion para el usuario que se acabo de crear para que la aplicacion sepa que usuario se tiene en la base de datos y sepamos que hace en nuestra aplicacion
                return redirect('tasks')
            except IntegrityError:#muestra el error que haya ocurrido internamente en la base de datos
                return render (request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'#se muestra este error solo si el usuario ya existe y nada más
                    })
        return render (request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Contraseña no coincide'
                    })
    
def tasks(request):
    return render(request, 'tasks.html')

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm()
        })
    else:
        print(request.POST)
        return render(request, 'create_task.html', {
        'form': TaskForm()
        })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:#aqui mira mos si el usurio que esta intentando ingresar esta de alguna manera bacio es decir que no tiene la autenticacion o no esta en la base de datos lanza un error
            return render(request, 'signin.html', {
        'form': AuthenticationForm,
        'error' : 'nombre o contraseña incorrecto '
    })
        else:
            login(request, user)#este login crea un tipo de autenticacion para el usuario que se acabo de crear para que la aplicacion sepa que usuario se tiene en la base de datos y sepamos que hace en nuestra aplicacion
            return redirect('tasks')
        
