from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from Afterword.settings import DEFAULT_FROM_EMAIL
import mimetypes


def send_confirm_email(confirm_email_url,email):    
    html_content = render_to_string('emails/confirm_email.html', {
        'confirm_email_url': confirm_email_url,
        'year': timezone.now().year,})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject='Afterword - Confirm Your Email',
        body=text_content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[email])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        print("email_views send_confirm_email done")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
 
def send_reset_password(reset_url, email):
    subject='Afterword - reset your password'
    html_content=render_to_string('emails/reset_pass_email.html', {
        'reset_url': reset_url,
        'year': timezone.now().year
    })
    text_content=strip_tags(html_content)    
    recipient=[email]
    from_email=DEFAULT_FROM_EMAIL

    msg=EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=recipient
    )
    msg.attach_alternative(html_content,"text/html")

    try:
        msg.send()
        print("email_views pass change email was successfully sent")
        return True
    except Exception as e:
        print(f"Error:{e}")
        return False


def send_message(letter):
    user=letter.author
    html_content=render_to_string('emails/send_message_email.html',
    {
        'first_name':user.first_name,
        'last_name':user.last_name,
        'subject': letter.subject,
        'message_content': letter.message,
        'sent_at': timezone.now(),
        'year': timezone.now().year
    })

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=letter.subject,
        body=text_content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[letter.receiver]
    )

    msg.attach_alternative(html_content, "text/html")

    if letter.attachment:
        try:
            letter.attachment.open('rb')
            file_content = letter.attachment.read()
            file_name = letter.attachment.name.split('/')[-1]
            import mimetypes
            mime_type, _ = mimetypes.guess_type(file_name)
            if not mime_type:
                mime_type = 'application/octet-stream'
            msg.attach(file_name, file_content, mime_type)
            letter.attachment.close()

        except Exception as e:
            print(f"Error attaching file: {e}")

    try:
        msg.send()
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False

    print("email_views status updated")
