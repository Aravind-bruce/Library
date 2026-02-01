from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_project, name="upload_project"),
    path("view/", views.view_projects, name="view_projects"),
    path("delete-project/<int:pk>/", views.delete_project, name="delete_project"),
    path('projects/download/<int:project_id>/', views.download_project, name='download'),
    path('submit_rating/', views.submit_project_rating, name='submit_project_rating'),

]
