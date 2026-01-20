# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Task, Request
from .forms import TaskForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from logic import solve

User = get_user_model()


@login_required
def index(request):
    """
    Обрабатывает ввод пользователя, создает Task и Request,
    и возвращает форму с заполненными данными
    """
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            # 1. Извлекаем данные из формы
            input_data = form.cleaned_data["input_data"]

            # 2. Обрабатываем данные (ваша бизнес-логика)
            # Здесь пример простой обработки - можно заменить на вашу логику
            task = process_input(input_data)

            # 4. Создаем запись в Request
            Request.objects.create(
                task=task, user=request.user, created_at=timezone.now()
            )

            # 5. Возвращаем ту же форму с заполненными данными
            return render(
                request,
                "index.html",
                {
                    "form": TaskForm(
                        initial={
                            "input_data": input_data,
                            "output_data": task.output_data,  # Это поле не в форме, но передаем в контекст
                        }
                    ),
                    "show_output": True,
                    "output_data": task.output_data,
                    "input_data": input_data,
                    "task_id": task.id,
                    "created_at": timezone.now(),
                },
            )

    else:
        form = TaskForm()

    return render(request, "index.html", {"form": form, "show_output": False})


def process_input(input_text):
    tasks = Task.objects.filter(input_data=input_text)

    # Проверка, есть ли такие задачи
    if tasks.exists():
        task = tasks[0]
        return task

    data = input_text.split()

    n = int(data[0])
    m = int(data[1])

    # Чтение массива котов
    c = list(map(int, data[2 : 2 + n]))

    # Чтение ребер
    edges = []
    idx = 2 + n
    for i in range(n - 1):
        x = int(data[idx])
        y = int(data[idx + 1])
        edges.append((x, y))
        idx += 2

    output_data = str(solve(n, m, c, edges))
    task = Task.objects.create(input_data=input_text, output_data=output_data)

    return task


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def protected_view(request):
    return render(request, "protected.html")


# Миксин для class-based views
class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = "protected.html"
