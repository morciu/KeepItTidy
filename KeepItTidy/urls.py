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
	path("collection_page/<int:collection_id>", views.collection_page, name="collection_page"),

	# API routes
	path("get_collections", views.get_collections, name="get_collections"),
	]

urlpatterns += staticfiles_urlpatterns()