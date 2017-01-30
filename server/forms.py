from .models import User, Image, File
from django import forms


class CustomUserCreationForm(forms.ModelForm):
    fb_id = forms.CharField(label='fb_id')
    fb_name = forms.CharField(label='fb_name')
    fb_token = forms.CharField(label='fb_token')
    fb_token_exp = forms.DateTimeField(label='fb_token_exp', widget=forms.SelectDateWidget)
    email = forms.EmailField(label='email')
    birth_date = forms.DateField(label='birth_date', widget=forms.SelectDateWidget)
    telephone = forms.CharField(label='tel')

    class Meta():
        model = User
        fields = fields = ['fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'email', 'telephone', 'birth_date']
        widgets = {
            'fb_token_exp': forms.DateTimeInput(),
            'birth_date': forms.DateInput(),
            'email': forms.EmailInput(),
        }


class UploadFileForm(forms.ModelForm):
    name = forms.CharField(required=False)
    class Meta:
        model = File
        fields = {'name', "path"}


class UploadImageForm(forms.ModelForm):
    name = forms.CharField(required=False)
    class Meta:
        model = Image
        fields = {'name', "path"}