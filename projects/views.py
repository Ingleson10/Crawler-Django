from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import openai
import os
from .models import Project, Schedule, URL, ScrapingRule
from .forms import ProjectForm, URLForm, ScrapingRuleForm, ScheduleForm

chave_openai = os.getenv('CHAVE_OPENAI')

@csrf_exempt
def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text:
            return JsonResponse({'error': 'Nenhum texto fornecido'}, status=400)

        try:
            openai.api_key = chave_openai
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                max_tokens=100
            )
            result = response.choices[0].text.strip()
            return JsonResponse({'analysis': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método de requisição inválido'}, status=400)

@csrf_exempt
def analyze_sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text:
            return JsonResponse({'error': 'Nenhum texto fornecido'}, status=400)

        try:
            openai.api_key = chave_openai
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Analyze the sentiment of the following text: '{text}'",
                max_tokens=50,
                stop="\n"
            )
            result = response.choices[0].text.strip()
            return JsonResponse({'sentiment': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método de requisição inválido'}, status=400)

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    urls = URL.objects.filter(project=project)
    schedules = Schedule.objects.filter(project=project)
    scraping_rules = ScrapingRule.objects.filter(project=project)
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        url_forms = [URLForm(request.POST, instance=url) for url in urls]
        schedule_forms = [ScheduleForm(request.POST, instance=schedule) for schedule in schedules]
        scraping_rule_forms = [ScrapingRuleForm(request.POST, instance=rule) for rule in scraping_rules]
        
        forms_valid = all([form.is_valid() for form in [project_form] + url_forms + schedule_forms + scraping_rule_forms])
        
        if forms_valid:
            project_form.save()
            for form in url_forms:
                form.save()
            for form in schedule_forms:
                form.save()
            for form in scraping_rule_forms:
                form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm(instance=project)
        url_forms = [URLForm(instance=url) for url in urls]
        schedule_forms = [ScheduleForm(instance=schedule) for schedule in schedules]
        scraping_rule_forms = [ScrapingRuleForm(instance=rule) for rule in scraping_rules]
    
    context = {
        'project': project,
        'urls': urls,
        'schedules': schedules,
        'scraping_rules': scraping_rules,
        'project_form': project_form,
        'url_forms': url_forms,
        'schedule_forms': schedule_forms,
        'scraping_rule_forms': scraping_rule_forms,
        'edit_mode': request.GET.get('edit', 'false') == 'true',
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'projects/project_detail_partial.html', context)
    else:
        return render(request, 'projects/project_detail.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    selected_project_id = request.GET.get('project_id')
    selected_project = None
    urls = []
    schedules = []
    scraping_rules = []

    if selected_project_id:
        selected_project = get_object_or_404(Project, id=selected_project_id, user=request.user)
        urls = URL.objects.filter(project=selected_project)
        schedules = Schedule.objects.filter(project=selected_project)
        scraping_rules = ScrapingRule.objects.filter(project=selected_project)
    
    context = {
        'projects': projects,
        'selected_project': selected_project,
        'urls': urls,
        'schedules': schedules,
        'scraping_rules': scraping_rules
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        url_forms = [URLForm(request.POST, prefix=str(i)) for i in range(len(request.POST.getlist('url')))]
        schedule_forms = [ScheduleForm(request.POST, prefix=str(i)) for i in range(len(request.POST.getlist('schedule')))]
        scraping_rule_forms = [ScrapingRuleForm(request.POST, prefix=str(i)) for i in range(len(request.POST.getlist('rule')))]
        
        forms_valid = project_form.is_valid() and all([form.is_valid() for form in url_forms + schedule_forms + scraping_rule_forms])
        
        if forms_valid:
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            
            for form in url_forms:
                url_instance = form.save(commit=False)
                url_instance.project = project
                url_instance.save()
                
            for form in schedule_forms:
                schedule_instance = form.save(commit=False)
                schedule_instance.project = project
                schedule_instance.save()
                
            for form in scraping_rule_forms:
                rule_instance = form.save(commit=False)
                rule_instance.project = project
                rule_instance.save()
            
            return redirect('project_list')
    else:
        project_form = ProjectForm()
        url_forms = [URLForm(prefix=str(i)) for i in range(1)]  # Inicializa com um formulário vazio
        schedule_forms = [ScheduleForm(prefix=str(i)) for i in range(1)]
        scraping_rule_forms = [ScrapingRuleForm(prefix=str(i)) for i in range(1)]
    
    context = {
        'project_form': project_form,
        'url_forms': url_forms,
        'schedule_forms': schedule_forms,
        'scraping_rule_forms': scraping_rule_forms,
    }
    return render(request, 'projects/project_create.html', context)
