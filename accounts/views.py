from django.shortcuts import render
from pack.methods.user_methods import *
from pack.functions.user_functions import *
from accounts.forms import *
from django.shortcuts import redirect
# Create your views here.


login = ''
password = ''


def user_name_and_password(**kwargs):
    global login, password
    if len(kwargs) == 0:
        return login, password
    else:
        login = str(kwargs.get('user_name'))
        password = str(kwargs.get('user_password'))


def registration(request):
    errors = []
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            question = form.cleaned_data.get('question')
            answer = form.cleaned_data.get('answer')
            user = UsersFunctions.get_user_by_login(login)
            if user is None:
                UserMethods.registration(login=login, password=password, question=question, answer=answer)
            else:
                errors.append('Пользователь с данным логином уже существует')
                return redirect('main_page')
    else:
        form = SignUpForm()
    return render(request, 'profile_html/registration.html', {'form': form,
                                                 'errors': errors})


def change_password(request):
    errors = []
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            question = form.cleaned_data.get('question')
            answer = form.cleaned_data.get('answer')
            user = UsersFunctions.get_user_by_login_and_password(login, password)
            if user is None:
                errors.append('Пароль или логин введены неверно')
            else:
                user_login = user_name_and_password()
                UserMethods.change_password(user_login[0], user_login[1], new_password, question, answer)
                return redirect('main_page')
    else:
        form = ChangePasswordForm()
    return render(request, 'profile_html/change_password.html', {'form': form,
                                                                'errors': errors})


def log_in(request):
    errors = []
    if request.method == 'POST':
        form = LogIn(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = UsersFunctions.get_user_by_login_and_password(login, password)
            if user is None:
                errors.append('Пароль или логин введены неверно')
            else:
                user_name_and_password(user_name=login,user_password=password)
                return redirect('main_page')
    else:
        form = LogIn()
    return render(request, 'profile_html/login.html', {'form': form,
                                          'errors': errors})


def log_out(request):
    global login, password
    login = ''
    password = ''
    return redirect('login')