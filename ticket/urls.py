from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.view, name="view"),
    path("fileUploads/", views.fileUpload, name="fileUpload")
]