from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

admin.site.register(Task, TaskAdmin)#aqui estoy agregando la clase Task que se creo en la carpeta de mi aplicacion, con el fin de que se pueda ver en la vista del admin que viene por defecto en django