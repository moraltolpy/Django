from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Ғылыми жұмыстың түрі әлі таңдалмады"

    class Meta:
        model = Article
        fields = ['title', 'subject', 'type']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 100, 'rows': 2}),
            'subject': forms.Textarea(attrs={'cols': 100, 'rows': 6})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Символдар саны 200-ден асты')

        return title

class AddStudentsForm(forms.ModelForm):
    class Meta:
        model = Foreign_Students
        fields = ['students']
        widgets = {'students': forms.NumberInput(attrs={'class': 'form-input'})}


class RegisterUserForm(UserCreationForm):
    last_name = forms.CharField(label='Тегіңіз', widget=forms.TextInput(attrs={'class': 'form-input','placeholder':''}))
    first_name = forms.CharField(label='Атыңыз', widget=forms.TextInput(attrs={'class': 'form-input','placeholder':''}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input','placeholder':''}))
    password1 = forms.CharField(label='Құпия сөз', widget=forms.PasswordInput(attrs={'class': 'form-input','placeholder':''}))
    password2 = forms.CharField(label='Құпия сөз(check)', widget=forms.PasswordInput(attrs={'class': 'form-input','placeholder':''}))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Құпия сөз', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
