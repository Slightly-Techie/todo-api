from django.urls import path
from . import views

urlpatterns = [
    path('get', views.todo_list, name='index'),
    path('create', views.create_todo, name='create_todo'),
    path('view/<int:todo_id>', views.view_todo, name='view todo'),
    path('update/<int:todo_id>', views.update_todo, name='updating_todo'),
    path('delete/<int:todo_id>', views.delete_todo, name='deleting_todo'),
    path('users', views.get_all_users, name='users'),
    path('signup', views.signup, name='signup_user'),
    path('login', views.login, name='login_user'),
    path('logout', views.logout, name='logout_user'),
    path('remove/<int:user_id>', views.delete_user, name='remove_user'),
    path('profile', views.user_profile, name='user_profile'),
]
