# Generated by Django 5.0.6 on 2024-07-18 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_options_alter_schedule_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ai_analysis',
            field=models.TextField(blank=True, null=True, verbose_name='Análise da IA'),
        ),
    ]
