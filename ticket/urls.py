from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.view, name="view"),
    path("file_scan/", views.file_scan, name="scan_file_upload"),
    path("file_upload/", views.file_upload, name="file_upload"),
    path("file_scan/<str:year>/<str:name>", views.download, name='download')
]