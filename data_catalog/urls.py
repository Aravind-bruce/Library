from django.urls import path
from . import views

urlpatterns = [
    path('view-logins/', views.view_logins, name='view_logins'),
]
