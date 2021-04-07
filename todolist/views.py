from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from .forms import TodoItemForm
from .serializers import TodoItemSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core import serializers
from django.template.loader import render_to_string


# Create your views here.
# class TodoList(APIView):
#     template_name = 'todolist/todo_list.html'

#     def get(self, request, format=None):
#         todos = TodoItem.objects.all()
#         serializer = TodoItemSerializer(todos, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = TodoItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def todo_list(request):
    # todos = TodoItem.objects.all()
    ctx = {}
    search = request.GET.get('q')
    if search:
        todos = TodoItem.objects.filter(Q(title__icontains = search)| Q(description__icontains = search))

    else:
        todos = TodoItem.objects.all()
        
    ctx["todos"] = todos

    if request.is_ajax():
        html = render_to_string(
            template_name="includes/list.html", 
            context={"todos": todos},
            request=request
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    if request.method == 'POST':
        todo = get_object_or_404(TodoItem, id=request.POST['todo_id'])
        todo.completed = not todo.completed
        todo.save()
        return redirect('/')
    return render(request, 'todolist/todo_list.html', context=ctx)


def todo_detail(request, id):
    todo = TodoItem.objects.get(id=id)

    if request.method == 'POST':        
        todo.completed = not todo.completed
        todo.save()
        return redirect(f'/{id}')
    context = {
        'todo': todo,
        }
    return render(request, 'todolist/todo_detail.html', context)


def create_todo(request):
    form = TodoItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'todolist/create_todo.html', context)

def update_todo(request, id):
    todo = TodoItem.objects.get(id=id)
    bound_form = TodoItemForm(request.POST or None, instance=todo)
    if bound_form.is_valid():
        bound_form.save()
        return redirect(f'/{id}')
    context = {
        'todo': todo,
        'form': bound_form,
        }
    return render(request, 'todolist/update_todo.html', context)

def delete_todo(request, id):
    todo = TodoItem.objects.get(id=id)
    if request.method == 'POST':
        todo.delete()
        return redirect('/')
    context = {
        'todo': todo
        }
    return render(request, 'todolist/delete_todo.html', context)

