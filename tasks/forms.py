from django import forms
from .models import Task

class TaskForm(forms.ModelForm):#aqui estamos reando una plantilla para nuestro html segun lo que necesitemos en la base de datos 
    class Meta:
        model = Task #aqui estoy diciendo que cuando se cree la pnatilla vamos a coger de modelo a la clase Task, para que funcione bien la plantilla con la clase y se pueda guardar los datos en la base de datos
        fields = ['title', 'description', 'important']#estos datos son los que se van a crear para la plantilla que son tambien los datos del models Task, para que todo quede bien creado
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo', }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe la tarea'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }