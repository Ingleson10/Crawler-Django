from django.core.management.base import BaseCommand
from projects.models import URL, URLScrapingRuleTemp

class Command(BaseCommand):
    help = 'Migrar dados de URL e ScrapingRule para URLScrapingRuleTemp'

    def handle(self, *args, **kwargs):
        for url in URL.objects.all():
            if  not url.new_selector:
                self.stdout.write(self.style.WARNING(f'URL {url.id} não tem um selector definido. Pulando...'))
                continue
            if  not url.new_type:
                self.stdout.write(self.style.WARNING(f'URL {url.id} não tem um type definido. Pulando...'))
                continue
            
            URLScrapingRuleTemp.objects.create(
                project=url.project,
                url=url.url,
                status=url.status,
                selector=url.new_selector,
                type=url.new_type,
                created_at=url.created_at
            )
        self.stdout.write(self.style.SUCCESS('Migração concluída com sucesso'))
