from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login, name="login"),
	path("register", views.register, name="register")
	]

urlpatterns += staticfiles_urlpatterns()