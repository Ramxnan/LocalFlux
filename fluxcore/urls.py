from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect


urlpatterns = [

    path('', views.homepage, name=''),
    path('homepage/', views.homepage, name='homepage'),
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    path('configure_outcomes/', views.configure_outcomes, name='configure_outcomes'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('homepage/', views.homepage, name='logout'),
    path('submit/', views.submit, name='submit'),
    path('upload_multiple_files_branch/', views.upload_multiple_files_branch, name='upload_multiple_files_branch'),
    path('upload_multiple_files_batch/', views.upload_multiple_files_batch, name='upload_multiple_files_batch'),
    path('download_file_generated/<str:file_name>/', views.download_file_generated, name='download_file_generated'),
    path('download_file_branch/<str:folder_name>/<str:file_name>/', views.download_file_branch, name='download_file_branch'),
    path('download_file_batch/<str:folder_name>/<str:file_name>/', views.download_file_batch, name='download_file_batch'),
    path('download_folder_branch/<str:folder_name>/', views.download_folder_branch, name='download_folder_branch'),
    path('download_folder_batch/<str:folder_name>/', views.download_folder_batch, name='download_folder_batch'),
    path('delete_generated/<str:file_name>/', views.delete_file_generated, name='delete_file_generated'),
    path('delete_folder_branch/<str:folder_name>/', views.delete_folder_branch, name='delete_folder_branch'),
    path('delete_folder_batch/<str:folder_name>/', views.delete_folder_batch, name='delete_folder_batch'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)