from django import forms
from .models import Project, URL, ScrapingRule, Schedule

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ['url', 'status']
        
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ScrapingRuleForm(forms.ModelForm):
    class Meta:
        model = ScrapingRule
        fields = ['selector', 'type']
        
        widgets = {
            'selector': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['frequency', 'next_run']
        
        widgets = {
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'next_run': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }
