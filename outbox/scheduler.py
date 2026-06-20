from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Letter
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta

scheduler = None

def send_scheduled_letters():
    print("checking letters...")

    now = timezone.now() + timedelta(hours=3,minutes=30)

    print("NOW:", now)
    for l in Letter.objects.all():
        print(l.id,"  ", l.scheduled_date, l.status)
        

    letters = Letter.objects.filter(
        status="scheduled",
        scheduled_date__lte=now
    )

    for letter in letters:
        try:
            send_mail(
                subject=letter.subject,
                message=letter.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[letter.receiver],
                fail_silently=False,
            )

            letter.status = "sent"
            letter.sent_date = now
            letter.save()

            print("sent:", letter.id)

        except Exception as e:
            letter.status = "failed"
            letter.save()
            print("error:", e)


def start_scheduler():
    global scheduler

    if scheduler:
        return

    print("scheduler started")

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_scheduled_letters,
        "interval",
        seconds=10,
        max_instances=1
    )
    scheduler.start()