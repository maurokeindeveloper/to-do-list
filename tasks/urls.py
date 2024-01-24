from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.signin, name="login"),
    path("logout/", views.signout, name="logout"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/pending", views.tasks_pending, name="tasks_pending"),
    path("tasks/completed", views.tasks_completed, name="tasks_completed"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/complete", views.complete_task, name="complete_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),
]
