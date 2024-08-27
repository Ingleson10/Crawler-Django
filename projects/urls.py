from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/delete-url/<int:url_id>/', views.delete_url, name='delete_url'),

    path('project/<int:project_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('project/<int:project_id>/csv/', views.generate_csv, name='generate_csv'),
    path('project/<int:project_id>/json/', views.generate_json, name='generate_json'),
    path('track-url/', views.track_url, name='track_url'),
]
