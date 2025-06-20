from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):#aqui estamos reando una plantilla para nuestro html segun lo que necesitemos en la base de datos 
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']#estos datos son los que se van a crear para la plantilla que son tambien los datos del models Task, para que todo quede bien creado