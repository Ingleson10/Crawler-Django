from django.db import models

class Plan(models.Model):

    MAX_SCRAPING_FREQUENCY_CHOICES = (
        ('daily', 'Diária'),
        ('weekly', 'Semanalmente'),
        ('monthly', 'Mensalmente'),
    )
    name = models.CharField(max_length=50, verbose_name='Plano')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    max_projects = models.IntegerField(verbose_name='Máximo de Projetos')
    max_urls = models.IntegerField(verbose_name='Máximo de Urls')
    max_scraping_frequency = models.CharField(max_length=20, choices=MAX_SCRAPING_FREQUENCY_CHOICES, verbose_name='Frequência Máxima de Scraping')

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'