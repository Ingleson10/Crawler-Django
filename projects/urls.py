from django.urls import path
from .views import analyze_text, analyze_sentiment, project_list, project_detail, project_create, generate_pdf, generate_csv, generate_json, track_url

urlpatterns = [
    path('', project_list, name='project_list'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project_create/', project_create, name='project_create'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('generate_csv/', generate_csv, name='generate_csv'),
    path('generate_json/', generate_json, name='generate_json'),
    path('track_url/', track_url, name='track_url'),
    path('analyze_text/', analyze_text, name='analyze_text'),
    path('analyze_sentiment/', analyze_sentiment, name='analyze_sentiment'),
]
