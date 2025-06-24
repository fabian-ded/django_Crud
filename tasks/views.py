from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#el "UserCreationForm" es para crear un usuario y el "AuthenticationForm" es para cpprobar si el usuario existe
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError #esta biblioteca funciona para mostrar los errores mas detallados que hayamos tenido en la base de datos es decir si estaba haciendo una consulta o enviado datos a este
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required #esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url
def tasks(request):#buscar tareas no cmpletadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)#aqui estoy haciendo un filtrado es dcir que solo me muestre los resultados del usuario que esta autenticado y ademas que solo me muestre las latareas que aun no se han completado osea no se han entregado fecha, todo eso esta en la base de datos
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required#esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url
def tasks_completed(request):#buscar tareas completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')#aqui estoy haciendo un filtrado es dcir que solo me muestre los resultados del usuario que esta autenticado y ademas que solo me muestre las latareas que aun no se han completado osea no se han entregado fecha, todo eso esta en la base de datos
    #ademas el 'order_by' es para ordenar en fecha desendente es decir desde la ultima hasta la primera
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required#esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url
def create_task(request):#crear tareas
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST)#aqui se contiene todos los datos que el usuario envió a través del formulario HTML,  Esto permite que Django valide esos datos y los prepare para ser guardados en la base de datos.
            new_tarea = form.save(commit=False)#aqui estoy teniendo con los datos validados del formulario, pero sin guardarla aún en la base de datos, porque se necesita el usuario que esta creando esta tarea es decir se necesita el usuario autenticado
            new_tarea.user = request.user #aqui estoy relacionando que en usuario que esta creando la tarea (new_tarea.user) es el mismo que está actualmente autenticado y ha iniciado sesión (request.user)
            #y ademas (new_tarea.user) se necesita para crear la tarea porque en la base de datos se tiene un forenkey de la tabla user y task etonces se necesita si o si el usuario
            new_tarea.save()#aqui se guardan todos los datos
            return redirect('tasks')# si todo salio exitoso esta linea se redirige a la vista de tasks
        except ValueError :
            return render(request, 'create_task.html', {
        'form': TaskForm(),
        'error': 'Por favor ingrese datos validos'
        })

@login_required#esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url
def task_detail (request, task_id):#actualizar tareas
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)#se hace una consulta con el metodo get, ademas siempre se debe colocar dentro de los parentesis la clase (base de datos) y el id el cual vamos a buscar, ademas el "user=request.user" es para que solo el usuario que esta utilizando la aplicacion pueda modificar sus tareas y no la de los demas
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)# ese request.user : representa al usuario que ha iniciado sesión en ese momento, Cuando un usuario se autentica (hace login), Django guarda su información y se puede acceder a ella fácilmente con "request.user".
            #ademas el pk=task_id: se utiliza explicitamente el "pk" Porque es un alias genérico del código lo cual lo hace más flexible y no le importa si la llave primaria se llama id, uuid, mi_llave_personalizada o etc..  con solo poner "pk" ya se sabe que es el id que identifica cada registro y es una buena practica.
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'Error actualizando tarea'
        })

@login_required#esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url    
def complete_task(request, task_id):#marcar una tarea
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()#aqui optengo el dato de la hora actual
        task.save()#aqui salvo la informacion que optuve y la mando a la base de datos o mejor dicho a la clase TASK que es lo mismo
        return redirect('tasks')

@login_required#esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url
def Eliminate_task(request, task_id):#eliminar tareas
    task = get_object_or_404(Task, pk=task_id, user=request.user)#se buscan las tareas del usuario
    if request.method == 'POST':#si en el html se esta utilizando el metodo 'POST' pues se ejecuta esta linea
        task.delete()#y aqui elimina lo que el usuario quiere eliminar
        return redirect('tasks')
    
@login_required#esta es una funcion de la biblioteca de django que nos permite que cualquier persona la cual no este autenticado no pueda ingresar a cualquier vista solo utilizando la url
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
        
