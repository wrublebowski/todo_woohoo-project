from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from todo_app.models import ToDo
from .forms import ToDoForm

def home(request):
    return render(request, "todo_app/home.html")

def signupuser(request):
    # if we don't click submit button in form with method="POST"
    if request.method == "GET":
        return render(request, "todo_app/signupuser.html", {'form':UserCreationForm()})
    else:
        # check if passwords are equal:
        if request.POST['password1']==request.POST['password2']:
            try:
                # create user object
                #  create_superuser(username, email=None, password=None, **extra_fields)
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
        if request.method == "GET":
            return render(request, "todo_app/loginuser.html", {'form':AuthenticationForm()})
        else:
            # authenticate(request, username=None, password=None, **kwargs)
            # if something goes wrong, user = None
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user == None:
                return render(request, "todo_app/loginuser.html", {'form':AuthenticationForm(), "message":"Invalid login or password"})
            else:
                login(request,user)
                return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currenttodos(request):
    # to show only current user's todos
    # to show only uncompleted todos (with no completiontime)
    all_todos = ToDo.objects.filter(user=request.user, completiontime__isnull=True)
    return render(request, "todo_app/currenttodos.html", {'all_todos':all_todos})

def createtodo(request):
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

def detail(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk)
    return render(request, 'todo_app/detail.html', {'todo':todo})
