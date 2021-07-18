from django.forms import inlineformset_factory
from .models import AdvUser, UserIp
from django import forms
from django.contrib.auth import password_validation

from django.contrib import messages


class RegisterUserForm(forms.ModelForm):
    """ Регистрация юзера через фронт , валидация пароля и Почта gmail.com и icloud.com не принимается """
    username = forms.CharField(max_length=25,label='Username')
    email = forms.EmailField(max_length=100, help_text='Почта gmail.com и icloud.com не принимается',
                             label='Адресс электроной почты')
    password = forms.CharField(min_length=7, max_length=17, label='Пароль', widget=forms.PasswordInput,
                               help_text='Пароль должен состоять из буквенно-цифровых символов, подчеркивания.'
                                         'Обязательно начинаться с прописной буквы.'
                                         'Длина от 7 до 16 символов')
    first_name = forms.RegexField(label='Имя', regex='^[A-Za-z-]+$')
    last_name = forms.RegexField(label='Фамилия',regex='^[A-Za-z-\s]+$')

    def valid_pass(self):
        password=self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        if self.cleaned_data.get('email').split('@')[1] == 'gmail.com' or self.cleaned_data.get('email').split('@')[1] == 'icloud.com':
            raise forms.ValidationError('Почта gmail.com и icloud.com не принимается')
        if self.cleaned_data.get('password')[0].islower() or self.cleaned_data.get('password')[0].isnumeric():
            raise forms.ValidationError('Обязательно начинаться с прописной буквы.')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserIpForm(forms.ModelForm):

    class Meta:
        model = UserIp
        fields = '__all__'
        ordering = ['-ip']
        list_filter = ('count_post', 'count_get')