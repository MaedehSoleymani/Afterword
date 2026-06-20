from django import forms
from accounts.models import C_User
from blog.models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','publish_date','status','img']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is your post about?'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }),
            'publish_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'img': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date < timezone.now():
            raise forms.ValidationError('Publish date cannot be in the past.')
        return publish_date