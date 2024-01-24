from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "Signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreationForm,
                        "error": "Ya existe un usuario con ese nombre",
                    },
                )
        else:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "error": "Las contraseñas no coinciden"},
            )


def signin(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {"form": AuthenticationForm, "error": "Usuario o contraseña inválidos"},
            )
        else:
            login(request, user)
            return redirect("tasks")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks.html", {"tasks": tasks, "status": "totales"})


@login_required
def tasks_pending(request):
    tasks_pending = Task.objects.filter(user=request.user, completed__isnull=True)
    return render(
        request, "tasks.html", {"tasks": tasks_pending, "status": "pendientes"}
    )


@login_required
def tasks_completed(request):
    tasks_completed = Task.objects.filter(
        user=request.user, completed__isnull=False
    ).order_by("-completed")
    return render(
        request,
        "tasks.html",
        {"tasks": tasks_completed, "status": "completadas"},
    )


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {
                    "task": task,
                    "form": form,
                    "error": "Se produjo un error al actualizar la tarea",
                },
            )


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Los datos ingresados son inválidos"},
            )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.completed = timezone.now()
        task.save()
        return redirect("tasks_completed")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
