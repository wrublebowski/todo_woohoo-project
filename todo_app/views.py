from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from todo_app.models import ToDo
from .forms import ToDoForm
from django.utils import timezone
# use login_required to prevent non logged users get inside.
# redirect them to login page with LOGIN_URL = '/loginpage' in settings.py
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "todo_app/home.html")

def signupuser(request):
    '''
    Creates an user object in data base.
    '''
    # if we don't click submit button in form with method="POST"
    if request.method == "GET":
        return render(request, "todo_app/signupuser.html", {'form':UserCreationForm()})
    else:
        # check if passwords are equal:
        if request.POST['password1']==request.POST['password2']:
            try:
                # create_user(username, email=None, password=None, **extra_fields)
                # go to web and 'inspect' to call values of name atribute
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # save user, login and redirect to path named 'current':
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, "todo_app/signupuser.html", {'form':UserCreationForm(), "message":"Username is already taken!"})

        else:
            # show the same view but with extra message from same dictionary
            return render(request, "todo_app/signupuser.html", {'form':UserCreationForm(), "message":"Passwords do not match!"})

def loginuser(request):
    '''
    Displays authentication form and checks if provided data is correct
    '''
    if request.method == "GET":
        return render(request, "todo_app/loginuser.html", {'form':AuthenticationForm()})
    else:
        # authenticate(request, username=None, password=None, **kwargs)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # if something goes wrong, user = None
        if user == None:
            return render(request, "todo_app/loginuser.html", {'form':AuthenticationForm(), "message":"Invalid login or password"})
        else:
            login(request,user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    '''
    Filters only current user's todos and only uncompleted
    '''
    all_todos = ToDo.objects.filter(user=request.user, completiontime__isnull=True)
    return render(request, "todo_app/currenttodos.html", {'all_todos':all_todos})

@login_required
def donetodos(request):
    '''
    Filters only done user's todos and only completed
    '''
    all_todos = ToDo.objects.filter(user=request.user, completiontime__isnull=False).order_by('-completiontime')
    return render(request, "todo_app/donetodos.html", {'all_todos':all_todos})

@login_required
def createtodo(request):
    '''
    Gives a custom form to fill, after submit it's been connected to user and saved
    '''
    if request.method == "GET":
        return render(request, "todo_app/createtodo.html", {'form':ToDoForm()})
    # if someone filled a form and submitted:
    else:
        # collect the form data:
        form = ToDoForm(request.POST)
        # dont commit (put in db) yet
        newtask = form.save(commit=False)
        # to connect newtask with a user
        newtask.user = request.user
        # save in database
        newtask.save()
        return redirect('currenttodos')

@login_required
def viewtodo(request, todo_pk):
    '''
    If it's a GET request: Grabs certain todo object and display form
    If it's a POST request: Saves the changes in todo object
    Provide: request and primary key of the object
    '''
    # to grab certain todo object by it's primary key (which gonna be id) from db
    # user=request.user <-- allows to display only logged user's todo :
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        # to display filled form of a chosen todo:
        form = ToDoForm(instance=todo)
        return render(request, 'todo_app/viewtodo.html', {'todo':todo, 'form':form})
    else:
        # to get request data (from submitted form in html)
        # we provide our request and todo instance:
        form = ToDoForm(request.POST, instance=todo)
        form.save()
        return redirect('currenttodos')

@login_required
def completetodo(request, todo_pk):
    '''
    A VIEW METHOD WITH NO TEMPLATE!
    Called by: action="{% url 'completetodo' todo.id %}" in viewtodo.html and path in urls.py
    Provide: request and primary key of the object
    '''
    # catch todo object from db
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.completiontime = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    '''
    A VIEW METHOD WITH NO TEMPLATE!
    Called by: action="{% url 'deletetodo' todo.id %}" in viewtodo.html and path in urls.py
    Provide: request and primary key of the object
    '''
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')
