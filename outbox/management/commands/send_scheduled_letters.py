

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from letters.models import Letter 
from pasnevesht.settings import DEFAULT_FROM_EMAIL

class Command(BaseCommand):
    help = 'ارسال خودکار پیام‌های زمان‌بندی شده'
    def handle(self, *args, **options):    
        now = timezone.now()    
        letters = Letter.objects.filter(
            status='scheduled',
            scheduled_date__lte=now)
        
        success_count = 0
        fail_count = 0

        for letter in letters:
            try:
                msg=send_mail(
                    subject=letter.subject,
                    body=letter.message,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=letter.receiver,
                    fail_silently=False)
                letter.status='sent'
                letter.save(update_fields=['status'])
                success_count+=1

                print('successfully sent')
                self.stdout.write(
                    self.style.SUCCESS(f'✓ ایمیل به {letter.receiver} فرستاده شد')
                )

            except Exception as e:
                letter.status='failed'
                letter.save(update_fields=['status'])
                fail_count+=1
                print(f"{e}")
                self.stdout.write(
                    self.style.ERROR(f'✗ خطا در ارسال به {letter.receiver}: {e}')
                )

        self.stdout.write(self.style.SUCCESS(
            f'\n--- نتیجه نهایی ---\n'
            f'موفق: {success_count}\n'
            f'ناموفق: {fail_count}\n'
            f'جمع کل: {success_count + fail_count}'
        ))