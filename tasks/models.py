from django.db import models
from django.contrib.auth.models import User #se importa la clase de usuario 

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True) #aqui estoy diciendo que sino se pasa nada en ese campo pues ese campo se puede quedar vacio
    created = models.DateTimeField(auto_now_add=True)#aqui vamos agregar la hora por defecto cuando se cree una tarea
    datecompleted = models.DateTimeField(null=True, blank=True)#aqui estoy diciendo que este campo iniciara vacio cuando se cree la tarea y ademas el "blank" significa que esta columna es opcional llenarla o completarla para el administrador
    important = models.BooleanField(default=False)#aqui estoy diciendo que todas las tareas que se vayan a crear no van a ser importante mas adelante las marcaremos como true
    user = models.ForeignKey(User, on_delete=models.CASCADE)#se hace la relacion de la clase User es decir, que se esta tabla de task se va a relacionar con la User en la base de datos
    
    def __str__(self):#este es una funcion que se utiliza para ver el titulo que viene de la base de datos para que se muestre en la vista del admin que viene por defecto de django
        return self.title + ' - para: ' + self.user.username
    
    