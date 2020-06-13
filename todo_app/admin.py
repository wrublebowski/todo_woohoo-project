from django.contrib import admin
from todo_app.models import ToDo

# if you have atribute that you can't edit but you can read in admin panel:
class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ['creationtime']

# Register your models here.
admin.site.register(ToDo, ToDoAdmin)
