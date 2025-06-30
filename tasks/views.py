# Replace your views.py with this:

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Task
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    tasks_todo = Task.objects.filter(user=request.user, status='todo').order_by('-created_at')
    tasks_doing = Task.objects.filter(user=request.user, status='doing').order_by('-created_at')
    tasks_completed = Task.objects.filter(user=request.user, status='completed').order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', 'todo')
        if title:
            Task.objects.create(user=request.user, title=title, status=status)
            return redirect('dashboard')

    context = {
        'tasks_todo': tasks_todo,
        'tasks_doing': tasks_doing,
        'tasks_completed': tasks_completed,
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@csrf_exempt
def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('status')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            if new_status in ['todo', 'doing', 'completed']:
                task.status = new_status
                task.save()
                return JsonResponse({'success': True})
        except Task.DoesNotExist:
            pass
    return JsonResponse({'success': False})

@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
    except Task.DoesNotExist:
        pass
    return redirect('dashboard')