from django.shortcuts import render, redirect
from .models import ToDo, User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializer import ToDoSerializer, UserSerializer
import jwt
import datetime
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def todo_list(request):
    token = request.COOKIES.get('jwt')
    if token:
        todos = ToDo.objects.all()
        if todos:
            serializer = ToDoSerializer(todos, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(status=400)
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['POST'])
def create_todo(request):
    token = request.COOKIES.get('jwt')
    if token:
        if request.method == 'POST':
            data = request.data
            serializer = ToDoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['GET'])
def view_todo(request, todo_id):
    token = request.COOKIES.get('jwt')
    if token:
        todo = ToDo.objects.filter(id=todo_id).first()
        if todo:
            serializer = ToDoSerializer(todo)
            return Response(serializer.data)
        else:
            return Response('Task not found', status=404)
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['PATCH'])
def update_todo(request, todo_id):
    token = request.COOKIES.get('jwt')
    if token:
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
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['DELETE'])
def delete_todo(request, todo_id):
    token = request.COOKIES.get('jwt')
    if token:
        todo = ToDo.objects.filter(id=todo_id).first()
        if todo:
            todo.delete()
            return Response('Task deleted successfully', status=200)
        else:
            return Response('Task not found', status=404)
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['GET'])
def get_all_users(request):
    token = request.COOKIES.get('jwt')
    if token:
        users = User.objects.all()
        if users:
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(status=400)
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['GET'])
def user_profile(request):
    token = request.COOKIES.get('jwt')
    if token:
        payload = jwt.decode(token, 'Thisisasecret', algorithms="HS256")
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        raise AuthenticationFailed('User not logged in')


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()
    print(user)

    if user is None:
        raise AuthenticationFailed('User not found')

    if not user.check_password(password):
        raise AuthenticationFailed('Invalid credentials')

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'Thisisasecret', algorithm="HS256")

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)

    response.data = {
        # "user": user['name'],
        "message": "Login successful",
        "jwt": token
    }
    return response


@api_view(['DELETE'])
def delete_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        user.delete()
        return Response({
            "message": "User deleted successfully"
        })
    else:
        return Response({
            "message": "User not found"
        })


@api_view(['POST'])
def logout(request):
    response = Response()

    response.delete_cookie('jwt')

    response.data = {
        'message': 'User logged out successfully'
    }

    return response
