from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='index'),
    path('api/create', views.create_todo, name='create_todo'),
    path('api/view/<int:todo_id>', views.view_todo, name='view todo'),
    path('api/update/<int:todo_id>', views.update_todo, name='updating_todo'),
    path('api/delete/<int:todo_id>', views.delete_todo, name='deleting_todo'),
]
