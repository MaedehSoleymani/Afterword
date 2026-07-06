# views.py - پیام‌های خطای رسمی

# خطای عمومی فرم
messages.error(request, 'An error occurred while processing your request. Please review the form and try again.')

# خطای اعتبارسنجی
messages.error(request, 'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')

# خطای سرور
messages.error(request, 'A technical issue prevented us from completing your request. Our team has been notified. Please try again later.')

# خطای دسترسی
messages.error(request, 'You do not have permission to perform this action. Please contact support if you believe this is an error.')


# موفقیت آمیز
messages.success(request, 'Your request has been processed successfully.')

# ذخیره شد
messages.success(request, 'The information has been saved successfully.')

# حذف شد
messages.success(request, 'The item has been permanently removed from the system.')

# بروزرسانی شد
messages.success(request, 'Your changes have been applied successfully.')

#ساخت اکانت 
if form.is_valid():
    form.save()
    messages.success(request, 'Your account has been created successfully. You may now log in using your credentials.')
else:
    messages.error(request, 'Unable to create your account. Please ensure all required fields are filled correctly and try again.')

if user is not None:
    login(request, user)
    messages.success(request, f'Welcome back, {user.username}. You have been logged in successfully.')
else:
    messages.error(request, 'Authentication failed. The username or password you entered is incorrect. Please try again.')

letter.delete()
messages.success(request, 'The message has been deleted successfully. This action cannot be undone.')

if check_password(current_password, request.user.password):
    request.user.set_password(new_password)
    request.user.save()
    messages.success(request, 'Your password has been changed successfully. Please use your new password for future logins.')
else:
    messages.error(request, 'Password change failed. The current password you entered is incorrect. Please try again.')

user.delete()
messages.success(request, 'Your account has been permanently deleted. We are sorry to see you go. You can always create a new account in the future.')

from django.http import JsonResponse

return JsonResponse({
    'success': False,
    'message': 'An error occurred while processing your request. Please try again.',
    'code': 'ERROR_001'
}, status=400)

def some_view(request):
    if something_went_wrong:
        messages.error(
            request, 
            'We encountered an issue while processing your request. '
            'Please review the information you provided and try again. '
            'If the problem persists, contact support.'
        )
    else:
        messages.success(
            request,
            'Operation completed successfully. Your changes have been saved.'
        )
    
    return redirect('some_url')
