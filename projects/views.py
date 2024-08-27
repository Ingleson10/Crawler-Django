import openai
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Project, Schedule, URLScrapingRule
from .forms import ProjectForm, URLScrapingRuleForm, ScheduleForm, URLFormSet, ScheduleFormSet
import csv
import json
from datetime import date
from reportlab.pdfgen import canvas
from django.forms import formset_factory, modelformset_factory
from django.forms import inlineformset_factory
# Obtenha a chave da OpenAI do settings.py
from django.conf import settings

@csrf_exempt
def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text:
            return JsonResponse({'error': 'Nenhum texto fornecido'}, status=400)

        try:
            openai.api_key = settings.CHAVE_OPENAI
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
            openai.api_key = settings.CHAVE_OPENAI
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
def project_create(request):

    URLFormSet = modelformset_factory(
        URLScrapingRule,
        form=URLScrapingRuleForm,
        extra=1,
    )
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        url_formset = URLFormSet(request.POST, queryset=URLScrapingRule.objects.none(), prefix='url')
        schedule_form = ScheduleForm(request.POST)

        if project_form.is_valid() and url_formset.is_valid() and schedule_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            
            for form in url_formset:
                url_instance = form.save(commit=False)
                url_instance.project = project
                url_instance.save()


            schedule_instance = schedule_form.save(commit=False)
            schedule_instance.project = project
            schedule_instance.created_at = date.today()
            schedule_instance.save()

            return redirect('project_list')

    else:
        project_form = ProjectForm()
        url_formset = URLFormSet(queryset=URLScrapingRule.objects.none(), prefix='url')
        schedule_form = ScheduleForm()

    context = {
        'project_form': project_form,
        'url_formset': url_formset,
        'schedule_form': schedule_form,
    }

    return render(request, 'projects/project_create.html', context)



@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    schedule, created = Schedule.objects.get_or_create(project=project)
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        url_formset = URLFormSet(request.POST, queryset=URLScrapingRule.objects.filter(project=project), prefix='url')
        schedule_form = ScheduleForm(request.POST, instance=project)

        
        if project_form.is_valid() and url_formset.is_valid() and schedule_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()

            url_formset.save(commit=False)
            for form in url_formset:
                url_instance = form.save(commit=False)
                if form.cleaned_data.get('DELETE'):
                    url_instance.delete()
                else:
                    url_instance.project = project
                    url_instance.save()

            schedule_instance  = schedule_form.save(commit=False)
            schedule_instance.project = project
            schedule_instance.save()


            return redirect('project_list')
    else:
        project_form = ProjectForm(instance=project)
        url_formset = URLFormSet(queryset=URLScrapingRule.objects.filter(project=project), prefix='url')
        schedule_form = ScheduleForm(instance=schedule)
        
    

    
    context = {
        'project_form': project_form,
        'url_formset': url_formset,
        'schedule_form': schedule_form,
    }

    return render(request, 'projects/project_edit.html', context)

@login_required
@require_POST
def delete_url(request, url_id):
    url_rule = get_object_or_404(URLScrapingRule, id=url_id, project__user=request.user)
    url_rule.delete()
    return JsonResponse({'status': 'success'})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    urls = URLScrapingRule.objects.filter(project=project)
    schedules = Schedule.objects.filter(project=project)

    context = {
        'project': project,
        'urls': urls,
        'schedules': schedules,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    selected_project_id = request.GET.get('project_id')
    selected_project = None
    urls = []
    schedules = []

    if selected_project_id:
        selected_project = get_object_or_404(Project, id=selected_project_id, user=request.user)
        urls = URLScrapingRule.objects.filter(project=selected_project)
        schedules = Schedule.objects.filter(project=selected_project)

    context = {
        'projects': projects,
        'selected_project': selected_project,
        'urls': urls,
        'schedules': schedules,
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def generate_pdf(request):
    project = Project.objects.filter(user=request.user).last()  # Apenas um exemplo, ajuste conforme necessário
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="project_{project.id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Projeto: {project.name}')
    p.drawString(100, 780, f'Descrição: {project.description}')
    p.drawString(100, 760, f'Análise da IA: {project.ai_analysis}')
    
    urls = URLScrapingRule.objects.filter(project=project)
    p.drawString(100, 740, 'URLs:')
    y = 720
    for url in urls:
        p.drawString(100, y, f'{url.url} - {url.get_status_display()}')
        y -= 20

    # Adicione outras seções conforme necessário
    
    p.showPage()
    p.save()
    return response

@login_required
def generate_csv(request):
    project = Project.objects.filter(user=request.user).last()  # Apenas um exemplo, ajuste conforme necessário
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="project_{project.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Projeto', project.name])
    writer.writerow(['Descrição', project.description])
    writer.writerow(['Análise da IA', project.ai_analysis])
    writer.writerow([])
    writer.writerow(['URLs'])
    urls = URLScrapingRule.objects.filter(project=project)
    for url in urls:
        writer.writerow([url.url, url.get_status_display()])

    # Adicione outras seções conforme necessário
    
    return response

@login_required
def generate_json(request):
    project = Project.objects.filter(user=request.user).last()  # Apenas um exemplo, ajuste conforme necessário
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="project_{project.id}.json"'

    data = {
        'project': {
            'name': project.name,
            'description': project.description,
            'ai_analysis': project.ai_analysis,
            'urls': [{'url': url.url, 'status': url.get_status_display()} for url in URLScrapingRule.objects.filter(project=project)],
            # Adicione outras seções conforme necessário
        }
    }
    
    response.write(json.dumps(data, indent=4))
    return response

@login_required
@csrf_exempt
def track_url(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        if not url:
            return JsonResponse({'error': 'Nenhuma URL fornecida'}, status=400)

        try:
            openai.api_key = settings.CHAVE_OPENAI
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Analyze the following URL: {url}",
                max_tokens=100
            )
            result = response.choices[0].text.strip()
            return JsonResponse({'analysis': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método de requisição inválido'}, status=400)
