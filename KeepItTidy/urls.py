from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("create_collection", views.create_collection, name="create_collection")
	]

urlpatterns += staticfiles_urlpatterns()