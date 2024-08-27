from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import Project, URLScrapingRule, Schedule

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class URLScrapingRuleForm(forms.ModelForm):
    class Meta:
        model = URLScrapingRule
        exclude = ['project', 'created_at']
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control', 'name': 'url[]'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'selector': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ['project', 'created_at']
        fields = ['frequency', 'next_run']
        labels = {
            'next_run': 'Próxima Execução',
        }
        widgets = {
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'next_run': forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

URLFormSet = modelformset_factory(URLScrapingRule, form=URLScrapingRuleForm, extra=0, can_delete=False)
ScheduleFormSet = formset_factory(ScheduleForm, extra=1)

