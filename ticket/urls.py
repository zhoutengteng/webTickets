from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.view, name="view"),
    path("file_scan/", views.file_scan, name="scan_file_upload"),
    path("file_upload/", views.file_upload, name="file_upload"),
    path("file_scan/<str:year>/<str:name>", views.download, name='download'),
    path("process_file", views.process_file, name='process_file'),
    path("progress_show", views.progress_show, name='progress_show'),
    path("progress_show_entry/", views.progress_show_entry, name='progress_show_entry'),
    path("progress_show_entry/<str:year>/<str:name>", views.download, name='download'),
]
