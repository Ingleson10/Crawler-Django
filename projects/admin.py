from django.contrib import admin
from .models import Project, URLScrapingRule, Schedule, ScrapingResult

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'user', 'created_at')
    search_fields = ('name', 'user__email')
    list_filter = ('created_at', 'user')
    date_hierarchy = 'created_at'

@admin.register(URLScrapingRule)
class URLScrapingRuleAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'status', 'created_at', 'url', 'selector', 'type')
    search_fields = ('url', 'project__name', 'selector')
    list_filter = ('status', 'created_at', 'project', 'type')
    date_hierarchy = 'created_at'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('project', 'frequency', 'next_run')
    search_fields = ('project__name',)
    list_filter = ('frequency', 'next_run', 'project')
    date_hierarchy = 'next_run'

@admin.register(ScrapingResult)
class ScrapingResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'scraped_at')
    search_fields = ('project__name',)
    list_filter = ('scraped_at', 'project')
    date_hierarchy = 'scraped_at'
