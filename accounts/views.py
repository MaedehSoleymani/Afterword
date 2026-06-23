#ACCOUNTS VIEWS

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import login as login_auth, authenticate, logout as logout_auth, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from accounts.models import C_User
from outbox.forms import LetterForm, ContactForm
from outbox.models import Letter, Contact
from accounts.forms import EditEmailForm, SignupForm, LoginForm, C_PasswordResetForm
from django.core.mail import send_mail, EmailMultiAlternatives
from Afterword.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import c_login_required, author_required, admin_required
from accounts.models import UserToken
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from datetime import timedelta
from django.contrib.sessions.models import Session

#----------------------------------------------------------
#views 
def signup(request):
    if request.user.is_authenticated:
        messages.error(request,'You Already Have An Account.')
        return redirect('accounts:dashboard')
    if request.method=='POST':
        form=SignupForm(request.POST)    
        if form.is_valid():
            pending_email=form.cleaned_data.get('email')
            if C_User.objects.filter(email=pending_email).exists():
                messages.error(request,"This email is accociated with another account. Please choose a different email.")
                return redirect("accounts:signup")
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            print(f"user saved but not active {user}")
            UserToken.objects.filter(user=user, token_type='verify_email', is_used=False).delete()
            token=UserToken.objects.create(
            user=user,
            token_type='verify_email',
            pending_email=pending_email)
            ok=send_confirm_email(request, pending_email, token, user)
            if ok:
                messages.success(request, f'A verification email has been sent to {pending_email}. Please check your inbox and spam folders. Click on the Link to create your account.')
                return redirect('accounts:login')
            else:
                messages.warning(request, f"Failed to send verification email to {pending_email}. Please try again.")
                return redirect('accounts:login')
        else:
            print(form.errors.as_json())
            messages.error(request,'Unable to create your account. Please ensure all required fields are filled correctly and try again.')
            return render(request, 'accounts/signup.html',{'form': form})
    else:
        form=SignupForm()
    return render(request,'accounts/signup.html',{'form':form})

def login(request):
    if request.user.is_authenticated:
        messages.error(request,'You Are Logged In.')
        return redirect('accounts:dashboard')
    if request.method== 'POST':
        remember_me=request.POST.get('remember_me')
        form= LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user=authenticate(request, email=email, password=password)
            if remember_me:
                request.session.set_expiry(7*24*60*60)
            else:
                request.session.set_expiry(0)
            if user:
                login_auth(request,user)
                if user.is_superuser:
                    return redirect('admin:index') 
                elif user.is_author:
                    return redirect('blog:author_dashboard')
                else:
                    messages.success(request,f'Welcome back, {user.email}. You have been logged in successfully.')
                    return redirect ('accounts:dashboard')
            else:
                messages.error(request,'wrong email or password. please try again.')
                return render(request, 'accounts/login.html', {'form': form})
        else:
            messages.error(request,'Authentication failed. The email or password you entered is incorrect. Please try again.')
            return redirect('accounts:login')
    else:
        form=LoginForm()
    return render(request,'accounts/login.html',{'form':form})

@c_login_required
def logout(request):
    logout_auth(request)
    return redirect('pages:home')

@c_login_required
def dashboard(request):
    #fetching data from DB
    user=request.user
    letter=Letter.objects.filter(author=user)
    total_messages=letter.count()
    scheduled_messages=letter.exclude(status='not_scheduled').count()
    unscheduled_messages=letter.filter(status='not_scheduled').count()
    registered_emails=Contact.objects.filter(user=user).count()
    context={'total_messages':total_messages,'scheduled_messages':scheduled_messages,
        'unscheduled_messages':unscheduled_messages,'registered_emails':registered_emails}
    return render (request,'accounts/dashboard_base.html',context)

@c_login_required
def add_message(request):
    user=request.user
    contacts= Contact.objects.filter(user=user).order_by('-created_date')
    if request.method=='POST':
        form=LetterForm(request.POST,request.FILES)
        if form.is_valid():
            letter=form.save(commit=False)
            letter.author=user
            send_option=form.cleaned_data.get("send_option")
            if send_option == 'not_scheduled':
                letter.status = Letter.STATUS_NOT_SCHEDULED
                letter.scheduled_date = None
            elif send_option == 'scheduled':
                letter.status = Letter.STATUS_SCHEDULED
            elif send_option == 'inactivity':
                letter.status = Letter.STATUS_INACTIVITY_TRIGGERED
                letter.send_on_inactivity=True
                letter.inactivity_days=form.cleaned_data.get('inactivity_days')
                letter.scheduled_date=None
            else:
                messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            
            letter.save()
            messages.success(request,'Your Message was saved successfully.')

            #create contact from Letter.email
            Contact.objects.get_or_create(
                user=user,
                email=letter.receiver,
                defaults={'name': ''}
            )
            return redirect('accounts:my_messages')
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return render (request,'accounts/dash_add_message.html',{'form':form, 'contacts':contacts})
    else:
        form=LetterForm()
    return render (request,'accounts/dash_add_message.html',{'form':form, 'contacts':contacts})

@c_login_required
def my_messages(request):
    letter=Letter.objects.filter(author=request.user)
    pending_letters=letter.exclude(status='sent').order_by('-created_date')
    sent_letters=letter.filter(status='sent').order_by('-created_date')
    return render(request,'accounts/dash_my_messages.html',{'pending_letters':pending_letters,'sent_letters':sent_letters})

@c_login_required
def letter_actions(request,lid):
    letter=get_object_or_404(Letter,author=request.user,id=lid)
    if request.method=='POST':
        action=request.POST.get("action")
        if action=="edit":
            return redirect('accounts:edit_message',lid=lid)
        elif action=="send":
            return redirect('accounts:send_message',lid=lid)
        elif action=="delete":
            letter.delete()
            messages.success(request,'The message has been deleted successfully.')
            return redirect('accounts:my_messages')
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return redirect('accounts:my_messages')
    return redirect('accounts:my_messages')
    
@c_login_required
def edit_message(request,lid):
    user=request.user
    letter=get_object_or_404(Letter,author=request.user,id=lid)
    contacts= Contact.objects.filter(user=user).order_by('-created_date')
    if request.method=='POST':
        form=LetterForm(request.POST, request.FILES, instance=letter)
        if form.is_valid():
            letter=form.save(commit=False)
            letter.author=user
            send_option=request.POST.get('send_option')
            inactivity_days=request.POST.get('inactivity_days')
            if send_option=='inactivity':
                letter.send_on_inactivity=True
                letter.inactivity_days = int(inactivity_days) if inactivity_days else 7
                letter.status=Letter.STATUS_INACTIVITY_TRIGGERED
                letter.scheduled_date=None
            elif send_option=='scheduled' and letter.scheduled_date:
                letter.send_on_inactivity=False
                letter.status=Letter.STATUS_SCHEDULED
            else:
                letter.send_on_inactivity=False
                letter.status=Letter.STATUS_NOT_SCHEDULED
                letter.scheduled_date=None
            if request.POST.get('clear_attachment'):
                if letter.attachment:
                    letter.attachment.delete(save=False)
                    letter.attachment = None
            letter.save()
            messages.success(request,'Your changes have been applied successfully.')
            return redirect('accounts:my_messages')
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return render(request, 'accounts/dash_edit_message.html', {'form': form, 'letter': letter, 'contacts':contacts})
    else:
        form=LetterForm(instance=letter)
    context={'letter':letter, 'form':form,'contacts': contacts}
    return render (request,'accounts/dash_edit_message.html',context)

@c_login_required
def contacts(request):
    contact=Contact.objects.filter(user=request.user)
    if request.method=='POST':
        action=request.POST.get('action')
        contact_id=request.POST.get('contact_id')

        if action=='add_contact':
            add_form=ContactForm(request.POST)
            if add_form.is_valid():
                new_contact=add_form.save(commit=False)
                new_contact.user=request.user
                new_contact.save()
                messages.success(request,'Your changes have been applied successfully.')
                return redirect('accounts:contacts')
            else:
                messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return redirect('accounts:contacts')
        
        elif action=='edit_contact':
            if contact_id:
                edit_contact=get_object_or_404(Contact, id=contact_id, user=request.user)
                edit_form=ContactForm(request.POST,instance=edit_contact)
                if edit_form.is_valid():
                    edit_form.save()
                    messages.success(request,'Your changes have been applied successfully.')
                else:
                    messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            else:
                messages.error(request, 'No contact specified for deletion.')
            return redirect('accounts:contacts')
    
        elif action=='delete_contact':
            if contact_id:
                del_contact=contact.filter(id=contact_id)
                del_contact.delete()
                messages.success(request,'Contact was succesfully deleted.')
                return redirect('accounts:contacts')
            else:
                messages.error(request, 'No contact specified for deletion.')
            return redirect('accounts:contacts')
        else:
            messages.error(request,'An error occurred while processing your request. Please review the form and try again.')
            return redirect('accounts:contacts')
    else:
        form=ContactForm()
    return render(request,'accounts/dash_contacts.html',{'contact':contact, 'form':form})


@c_login_required
def account_settings(request):
    user=request.user
    if request.method=='POST':
        action=request.POST.get('action')
        email_form=EditemailForm(request.POST, instance=user)
        if action=='change_email':
            if email_form.is_valid():
                new_email = email_form.cleaned_data['email']
                if User.objects.filter(email=new_email).exists():
                    messages.error(request, 'This email is already registered to another account.')
                    return redirect('accounts:account_settings')                
                UserToken.objects.filter(user=user, token_type='verify_email', is_used=False).delete()            
                user_token= UserToken.objects.create(
                user=user,
                token_type='verify_email',
                pending_email=new_email)
                result=send_confirm_email(request, new_email, user_token, user)
                if result:
                    messages.success(request, f'Verification email sent to {new_email}. Please check your inbox and spam folders.')
                else:
                    messages.error(request, f'Failed to send verification email to {new_email}.')
            else:
                email_form=EditEmailForm()

                    
        elif action=='change_password':
            try:
                UserToken.objects.filter(user=user, token_type='verify_email', is_used=False).delete()            
                user_token= UserToken.objects.create(
                    user=user,
                    token_type='reset_password')
                ok=send_reset_password(request, user_token.token, user)
                if ok:
                    messages.success(request, f'Password reset link has been sent to {user.email}. Please check your inbox.')
                else:
                    messages.error(request, f'Failed to send verification email to {user.email}.')
            except Exception as e:
                messages.error(request,'Something went wrong. please try again.')
                print(f"{e}")
                return redirect('accounts:account_settings')
            
        elif action=='delete_account':
             logout_auth(request)
             user.delete()
             messages.success(request,'Your account has been permanently deleted. We are sorry to see you go. You can always create a new account in the future.')
             return redirect('pages:home')
        else:
            messages.error(request, 'Invalid action.')
            return redirect('accounts:account_settings')
    else:
        email_form=EditEmailForm(instance=user)

    context = {
    'email_form': email_form,'email_form': email_form,}
    return render(request,'accounts/dash_account_settings.html',context)


def send_confirm_email(request, pending_email, token, user):    
    confirm_email_url= request.build_absolute_uri(
    reverse('accounts:receive_confirm_email', kwargs={'token': token.token}))
    print("before render to string send_confirm_email")
    html_content = render_to_string('emails/confirm_email.html', {
        'confirm_email_url': confirm_email_url,
        'year': timezone.now().year,})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject='Afterword - Confirm Your Email',
        body=text_content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[pending_email])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        print("send_confirm_email done")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def receive_confirm_email(request,token):
    user_token=get_object_or_404(UserToken, token=token, token_type='verify_email')
    if not user_token.is_valid():
        messages.error(request, 'Link expired or already used.')
        return redirect('accounts:account_settings')
    user=user_token.user
    user.is_active=True
    user.save(update_fields=['is_active'])
    print("user is active now")
    user_token.is_used = True
    user_token.save(update_fields=['is_used'])
    messages.success(request, 'Email verified, your account was created successfully.')
    return redirect('accounts:login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'No account found with this email address.')
            return redirect('accounts:forgot_password')       
        UserToken.objects.filter(user=user, token_type='reset_password', is_used=False).delete()       
        user_token= UserToken.objects.create(
            user=user,
            token_type='reset_password'
        )
        try: 
            send_reset_password(request, user_token.token, user)        
            messages.success(request, f'Reset link sent to {email}. Please check your inbox and spam folders.')
        except Exception as e:
            messages.error(request, f'Failed to send an Email.')
            print(f"{e}")
    return render(request, 'accounts/login_forgot_password.html')

    
def send_reset_password(request, token, user):
    reset_url= request.build_absolute_uri(
    reverse('accounts:receive_reset_password', kwargs={'token': token}))

    subject='Afterword - reset your password'
    html_content=render_to_string('emails/reset_pass_email.html', {
        'reset_url': reset_url,
        'year': timezone.now().year
    })
    text_content=strip_tags(html_content)    
    recipient=[user.email]
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
        print("pass change email was successfully sent")
        return True
    except Exception as e:
        print(f"Error:{e}")
        return False


def receive_reset_password(request, token):
    user_token=get_object_or_404(UserToken,token=token,token_type='reset_password')
    user=user_token.user
    if not user_token.is_valid():
        messages.error(request,'The link has expired or already used.')
        return redirect('accounts:reset_password')
    if request.method=='POST':
        form=C_PasswordResetForm(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            confirm_password=form.cleaned_data['confirm_password']
            if user.check_password(new_password):
                messages.error(request,'New password cannot be the same as your current password.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password)
                user.save(update_fields=['password'])
                update_session_auth_hash(request, user)            
                user_token.is_used=True
                user_token.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('accounts:login')
        else:
            messages.error(request,'Please correct the errors.')
    else:
        form=C_PasswordResetForm()
    return render(request, 'accounts/reset_password.html', {'form':form,'token':token})


@c_login_required
def send_message(request, lid):
    letter=get_object_or_404(Letter,author=request.user,id=lid)

    html_content=render_to_string('emails/send_message_email.html',
    {
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
            messages.warning(request, "Message sent but attachment failed.")

    try:
        msg.send()
        print("email sent")
        letter.status=Letter.STATUS_SENT
        print("email status changed")
        letter.sent_date=timezone.now()
        print("sent date set")
        messages.success(request, "Message sent successfully.")
    except Exception as e:
        print(f"Email send error: {e}")
        letter.status=Letter.STATUS_FAILED
        messages.error(request, "Failed to send message.")

    letter.save()
    print("status updated")

    return redirect('accounts:my_messages')

