from django.urls import path, include
from . import views
    
app_name = 'todo'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    # path('', views.TodoList.as_view(), name='todo_list'),
    path('<int:id>/', views.todo_detail, name='todo_detail'),
    path('create/', views.create_todo, name='create_todo'),
    path('<int:id>/update/', views.update_todo, name='update_todo'),
    path('<int:id>/delete/', views.delete_todo, name='delete_todo'),
]