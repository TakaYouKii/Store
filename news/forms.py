from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', help_text='''Имя пользователя должно состаять максимум из 150 
                                                                       символов''', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='''Имя пользователя должно состаять максимум из 150 
                                                                   символов''', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published','photo', 'category']
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea(),
            'category': forms.Select(),
            'photo': forms.FileInput()
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d',title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title


# alt+j
# ctrl+shift+alt+j