from django.urls import path
from . import views


urlpatterns = [
	path("test/", views.test.as_view(),name="test"),
	path("register/",views.RegisterView.as_view(),name="register-view"),
	path("login/",views.LoginView.as_view(),name="login-view"),
	path("task/",views.TaskView.as_view(),name="tasks"),
	path("task-update/",views.TaskUpdate.as_view(),name="Task-Update"),
	path("task/<str:keyword>/",views.TaskFilter.as_view(),name="Task-filter")
]