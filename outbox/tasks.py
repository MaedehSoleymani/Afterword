from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from accounts.email_views import send_confirm_email, send_reset_password, send_message


@shared_task(bind=True, max_retries=3)
def send_confirm_email_task(self,confirm_email_url, email):
    try:
        return send_confirm_email(confirm_email_url,email)
    except Exception as e:
        print(f"Retrying confirm email: {e}")
        raise self.retry(exc=exc, countdown=30)


@shared_task(bind=True, max_retries=3)
def send_reset_password_task(self,reset_url,email):
    try:
        return send_reset_password(reset_url,email)
    except Exception as e:
        print(f"Retrying reset password: {e}")
        raise self.retry(exc=e, countdown=30)


@shared_task(bind=True, max_retries=3)
def send_message_task(self, letter):
    try:
        return send_message(letter)
    except Exception as e:
        print(f"Retrying message send: {e}")
        raise self.retry(exc=e, countdown=30)


@shared_task
def send_due_messages():
    from outbox.models import Letter
    now = timezone.now()
    due_messages = Letter.objects.filter(
        status=Letter.STATUS_SCHEDULED,
        scheduled_date__lte=now)
    sent_count = 0
    failed_count = 0
    for letter in due_messages:
        try:
            send_message(letter)
            letter.status = Letter.STATUS_SENT
            letter.sent_date = now
            letter.save(update_fields=['status', 'sent_date'])
            sent_count += 1
            print(f"✓ Sent scheduled message {letter.id} to {letter.receiver}")
        except Exception as e:
            letter.status = Letter.STATUS_FAILED
            letter.save(update_fields=['status'])
            failed_count += 1
            print(f"✗ Failed to send message {letter.id}: {e}")
    
    return f"Processed: {sent_count} sent, {failed_count} failed"


@shared_task
def check_inactive_users():
    from outbox.models import Letter
    now = timezone.now()
    triggered_count = 0
    inactivity_messages = Letter.objects.filter(
        status=Letter.STATUS_INACTIVITY_TRIGGERED,
        send_on_inactivity=True)
    
    for letter in inactivity_messages:
        user = letter.author
        inactivity_threshold = now - timedelta(days=letter.inactivity_days)        
        last_activity = getattr(user, 'last_activity', None) or user.date_joined
        if last_activity < inactivity_threshold:
            try:
                send_message(letter)
                letter.status = Letter.STATUS_SENT
                letter.sent_date = now
                letter.inactivity_triggered_at = now
                letter.save(update_fields=['status', 'sent_date', 'inactivity_triggered_at'])
                triggered_count += 1
                print(f"Triggered inactivity message {letter.id} for user {user.email}")
            except Exception as e:
                letter.status = Letter.STATUS_FAILED
                letter.save(update_fields=['status'])
                print(f"✗ Failed: {e}")
    
    return f"Triggered {triggered_count} inactivity messages"