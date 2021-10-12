from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Required for displaying images in the media folder
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	# Index
	path("", views.index, name="index"),

	# User
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),

	# Collection
	path("create_collection", views.create_collection, name="create_collection"),
	path("view_collection", views.view_collection, name="view_collection"),
	path("view_collection/<int:collection_id>", views.view_collection, name="view_collection"),
	path("delete_collection/<int:collection_id>", views.delete_collection, name="delete_collection"),

	# Item
	path("add_item/<int:collection_id>", views.add_item, name="add_item"),
	path("delete_item", views.delete_item, name="delete_item"),
	path("edit_item/<int:item_id>", views.edit_item, name="edit_item"),

	# API routes
	path("get_collections", views.get_collections, name="get_collections"),
	]

urlpatterns += staticfiles_urlpatterns()

# Setting up url to serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)