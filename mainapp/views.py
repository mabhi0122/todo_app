from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TodoForm, UpdateTodoForm
from .models import Todo
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

# todo home/ task list page
def todo_tasks(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                return redirect('todo_list')
            else:
                messages.error(request, 'Not a user. Please login...')
                return redirect('todo_list')
    else:
        form = TodoForm()

    if request.user.is_authenticated:
        tasks = Todo.objects.filter(user=request.user).order_by('-id')
        count = tasks.filter(is_completed=False).count()
    else:
        tasks = []
        count = 0
        # tasks = Todo.objects.filter(user = request.user).order_by('-id')
        # count = Todo.objects.filter(is_completed=False).count()
    context = {
        'form': form,
        'count': count,
        'todo_list': tasks
    }
    return render(request, 'mainapp/todo_list_view.html', context)


# task detail view
class DetailTaskView(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = 'details'
    template_name = 'mainapp/detail_view.html'


# updating toggle button
@login_required
def update_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed = request.POST.get('completed') == 'true'
        task = get_object_or_404(Todo, id=task_id)
        task.is_completed = completed
        task.save()
        return JsonResponse({'id': task.id, 'title': task.title, 'completed': task.is_completed})
    return JsonResponse({'error': 'Invalid request method'})


# task edit view
class UpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        task_id = get_object_or_404(Todo, pk=id)
        updateform = UpdateTodoForm(instance=task_id)
        return render(request, 'mainapp/update_task.html', {'updateform': updateform})

    def post(self, request, id):
        if request.method == "POST":
            task_id = get_object_or_404(Todo, pk=id)
            form = UpdateTodoForm(request.POST, instance=task_id)
            if form.is_valid():
                # new_title = form.cleaned_data['title']
                # task_id.update_title(new_title)
                form.save()
                messages.success(request, 'task updated sucessfully...')
                return redirect('todo_list')
        return redirect('todo_list')


# task delete view
class DeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        task_id = get_object_or_404(Todo, pk=id)
        return redirect('todo_list')

    def post(self, request, id):
        if request.method == "POST":
            task_id = get_object_or_404(Todo, pk=id)
            task_id.delete()
            messages.success(request, 'task deleted')
            return redirect('todo_list')


# completed tasks view
def completed_tasks(request):
    if request.user.is_authenticated:
        form = TodoForm()
        if request.user.is_authenticated:
            completed = Todo.objects.filter(user=request.user, is_completed=True).order_by('-id')
            count = completed.filter(is_completed=True).count()
        else:
            completed = []
            count = 0
        context = {'completed': completed, 'count': count, 'form': form}
        return render(request, 'mainapp/completed_tasks.html', context)
    else:
        return redirect('/')


# incompleted tasks view
def incompleted_tasks(request):
    if request.user.is_authenticated:
        form = TodoForm()
        if request.user.is_authenticated:
            completed = Todo.objects.filter(user=request.user, is_completed=False).order_by('-id')
            count = completed.filter(is_completed=False).count()
        else:
            completed = []
            count = 0

        context = {'completed': completed, 'count': count, 'form': form}
        return render(request, 'mainapp/incompleted_tasks.html', context)
    else:
        return redirect('/')
