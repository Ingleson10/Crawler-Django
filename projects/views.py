from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Schedule, URL, ScrapingRule
from .forms import ProjectForm

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    urls = URL.objects.filter(project=project)
    schedules = Schedule.objects.filter(project=project)
    scraping_rules = ScrapingRule.objects.filter(project=project)
    
    context = {
        'project': project,
        'urls': urls,
        'schedules': schedules,
        'scraping_rules': scraping_rules
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
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})
