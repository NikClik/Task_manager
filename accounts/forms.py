from django import forms


class SignUpForm(forms.Form):
    login = forms.CharField(max_length=30, min_length=4, label='Логин')
    password = forms.CharField(max_length=12, min_length=4, label='Пароль')
    question = forms.CharField(max_length=30, min_length=2, label='Секретный вопрос')
    answer = forms.CharField(max_length=30, min_length=2, label='Ответ на вопрос')


class ChangePasswordForm(forms.Form):
    login = forms.CharField(max_length=30, min_length=4, label='Логин')
    password = forms.CharField(max_length=12, min_length=4, label='Пароль')
    new_password = forms.CharField(max_length=12, min_length=4, label='Пароль')
    question = forms.CharField(max_length=30, min_length=2, label='Секретный вопрос')
    answer = forms.CharField(max_length=30, min_length=2, label='Ответ на вопрос')


class LogIn(forms.Form):
    login = forms.CharField(max_length=30, min_length=4, label='Логин')
    password = forms.CharField(max_length=12, min_length=4, label='Пароль')