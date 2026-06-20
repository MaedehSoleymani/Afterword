from django import forms
from .models import Letter,Contact
from django.utils import timezone

class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        fields=['name','email']

        widgets={
            'name':forms.TextInput(),
            'email':forms.EmailInput()
        }

class LetterForm(forms.ModelForm):
    send_option = forms.ChoiceField(
    choices=[
            ('not_scheduled', 'Save without scheduling'),
            ('scheduled', 'Schedule for specific date/time'),
            ('inactivity', 'Send if I\'m inactive for X days'),
        ],
        widget=forms.RadioSelect,
        initial='not_scheduled')
    inactivity_days = forms.IntegerField(
        min_value=1,
        max_value=365,
        initial=7,
        required=False,
        help_text="Number of days of inactivity before sending")

    class Meta:
        model= Letter
        fields= ['receiver', 'subject', 'message','scheduled_date']

        widgets={
            'receiver':forms.EmailInput(),
            'subject':forms.TextInput(),
            'message':forms.Textarea(),
            'scheduled_date':forms.DateTimeInput(
                attrs={'type': 'datetime-local'})}

    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data.get('scheduled_date')
        if scheduled_date and scheduled_date < timezone.now():
            raise forms.ValidationError('You cannot schedule a message in the past. Please select a future date and time.')
        return scheduled_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        send_option = cleaned_data.get('send_option')
        scheduled_date = cleaned_data.get('scheduled_date')
        inactivity_days = cleaned_data.get('inactivity_days')
        if send_option == 'scheduled' and not scheduled_date:
            self.add_error('scheduled_date', 'Please select a date/time for scheduled messages.')
        if send_option == 'inactivity' and not inactivity_days:
            self.add_error(None, 'Please specify the number of days for inactivity trigger.')
        return cleaned_data
