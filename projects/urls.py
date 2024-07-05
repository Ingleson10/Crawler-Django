# urls.py

from django.urls import path
from .views import analyze_text, analyze_sentiment, project_list, project_detail, project_create

urlpatterns = [
    # URL para a análise de texto
    path('analyze_text/', analyze_text, name='analyze_text'),
    
    # URL para a análise de sentimento
    path('analyze-sentiment/', analyze_sentiment, name='analyze_sentiment'),
    
    # URLs relacionadas aos projetos
    path('', project_list, name='project_list'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/create/', project_create, name='project_create'),
]