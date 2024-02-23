from django.shortcuts import render, redirect
from .models import ToDo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializer import ToDoSerializer


@api_view(['GET'])
def todo_list(request):
    todos = ToDo.objects.all()
    if todos:
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response(status=400)


@api_view(['POST'])
def create_todo(request):
    if request.method == 'POST':
        data = request.data
        serializer = ToDoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


@api_view(['GET'])
def view_todo(request, todo_id):
    todo = ToDo.objects.filter(id=todo_id).first()
    if todo:
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)
    else:
        return Response('Task not found', status=404)


@api_view(['PATCH'])
def update_todo(request, todo_id):
    todo = ToDo.objects.filter(id=todo_id).first()
    if todo:
        data = request.data
        serializer = ToDoSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response('Todo not found', status=404)


@api_view(['DELETE'])
def delete_todo(request, todo_id):
    todo = ToDo.objects.filter(id=todo_id).first()
    if todo:
        todo.delete()
        return Response('Task deleted successfully', status=200)
    else:
        return Response('Task not found', status=404)
