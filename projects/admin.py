from django.contrib import admin
from .models import Project, URL, ScrapingRule, Schedule, ScrapingResult

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__email')
    list_filter = ('created_at', 'user')
    date_hierarchy = 'created_at'

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('project', 'status', 'created_at','url')
    search_fields = ('url', 'project__name')
    list_filter = ('status', 'created_at', 'project')
    date_hierarchy = 'created_at'

@admin.register(ScrapingRule)
class ScrapingRuleAdmin(admin.ModelAdmin):
    list_display = ('selector', 'type', 'project', 'created_at')
    search_fields = ('selector', 'project__name')
    list_filter = ('type', 'created_at', 'project')
    date_hierarchy = 'created_at'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('project', 'frequency', 'next_run')
    search_fields = ('project__name',)
    list_filter = ('frequency', 'next_run', 'project')
    date_hierarchy = 'next_run'

@admin.register(ScrapingResult)
class ScrapingResultAdmin(admin.ModelAdmin):
    list_display = ('id','url', 'scraped_at')
    search_fields = ('url__url',)
    list_filter = ('scraped_at', 'url')
    date_hierarchy = 'scraped_at'
