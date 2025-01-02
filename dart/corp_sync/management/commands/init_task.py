from django.core.management.base import BaseCommand
from corp_sync.models import CompanyInfo, History, CorpCode

class Command(BaseCommand):
    help = "Initialize pending corp codes in the history table."

    def handle(self, *args, **kwargs):
        # 모든 corp_code 값을 가져옵니다.
        corp_codes = CorpCode.objects.all().values_list("corp_code", flat=True)
        
        count = 0
        for corp_code in corp_codes:
            # 이미 있는 항목은 건너뜁니다.
            _, created = History.objects.get_or_create(
                corp_code=corp_code,
                defaults={
                    'status': 'pending',
                    'retry_count': 0,
                    'last_called_date': None
                }
            )
            if created:
                count += 1

        # 결과 출력
        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {count} corp codes'))