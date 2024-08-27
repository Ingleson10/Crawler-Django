from django.db import models
from accounts.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    name = models.CharField(max_length=100, null=False, verbose_name='Nome do Projeto')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    ai_analysis = models.TextField(null=True, blank=True, verbose_name='Análise da IA')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return f'{self.pk} - {self.name}'


class URLScrapingRule(models.Model):

    STATUS_CHOICES = (
        ('valid', 'Válida'),
        ('invalid', 'Inválida'),
    )

    TYPE_CHOICES = (
        ('CSS', 'CSS'),
        ('XPath', 'XPath'),
    )

    project = models.ForeignKey(Project, related_name='urls', on_delete=models.CASCADE, verbose_name='Projeto')
    url = models.TextField(null=False, verbose_name='URL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    selector = models.TextField(null=False, verbose_name='Seletor')
    type = models.CharField(max_length=20, null=False, choices=TYPE_CHOICES, verbose_name='Tipo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Regra de Scraping de URL'
        verbose_name_plural = 'Regras de Scraping de URL'

    def __str__(self):
        return f'{self.project} - {self.url}'


class Schedule(models.Model):
    
    FREQUENCY_CHOICES = (
        ('daily', 'Diária'),
        ('weekly', 'Semanalmente'),
        ('monthly', 'Mensalmente'),
    )
    project = models.ForeignKey(Project, related_name='schedules', on_delete=models.CASCADE, verbose_name='Projeto')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Frequência')
    next_run = models.DateTimeField(verbose_name='Próxima Execução')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'


class ScrapingResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Projeto')
    data = models.JSONField(null=False, verbose_name='Resultado')
    scraped_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Resultado de Scraping'
        verbose_name_plural = 'Resultados de Scraping'

    def __str__(self):
        return f'{self.pk} - {self.project}'