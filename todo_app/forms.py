from django.forms import ModelForm
from todo_app.models import ToDo

# HERE WE CONNECT A FORM DATA WITH MODEL
# create new form class and inherit from ModelForm
class ToDoForm(ModelForm):
    # provide model to work with:
    class Meta:
        model = ToDo
        # choose fields to show:
        fields = ['task', 'description', 'important']
