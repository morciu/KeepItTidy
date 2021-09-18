from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("create_collection", views.create_collection, name="create_collection"),
	path("view_collection", views.view_collection, name="view_collection"),
	path("view_collection/<int:collection_id>", views.view_collection, name="view_collection"),
	path("add_item/<int:collection_id>", views.add_item, name="add_item"),

	# API routes
	path("get_collections", views.get_collections, name="get_collections"),
	]

urlpatterns += staticfiles_urlpatterns()