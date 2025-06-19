from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError #esta biblioteca funciona para mostrar los errores mas detallados que hayamos tenido en la base de datos es decir si estaba haciendo una consulta o enviado datos a este
from django.http import HttpResponse


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
                login(request, user)#este login crea un topo de autenticacion para el usuario que se acabo de crear para que la aplicacion sepa que usuario se tiene en la base de datos y sepamos que hace en nuestra aplicacion
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

def signout(request):
    logout(request)
    return redirect('home')