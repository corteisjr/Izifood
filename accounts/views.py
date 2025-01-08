from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            user_record = None
            try:
                user_record = User.objects.get(email=cf['email'])
            except User.DoesNotExist:
                pass
            if user_record:
                user = authenticate(request, username=user_record, password=cf['password'])
                if user is not None:
                    login(request, user)
                    return redirect('product_list')
                else:
                    form.add_error(None, 'Invalid password')
            messages.error(request, 'Email ou senha inválidos')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cf = user_form.cleaned_data
            
            email = cf['email']
            password = cf['password']
            password2 = cf['password2']
            
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request,
                        "Já existe um usuário com este email!!"
                    )
                    return render(
                        request,
                        'accounts/register.html',
                        {'user_form': user_form}
                    )
            else:
                messages.error(
                    request,
                    'As senhas não combinam!!'
                )
                return render(
                    request, 
                    'accounts/register.html',
                    {'user-form': user_form}
                )
            new_user = User.objects.create_user(
                first_name = cf['first_name'],
                last_name = cf['last_name'],
                username=email,
                password=password
            )
            return render(
                request,
                'accounts/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
        return render (
            request,
            'accounts/register.html',
            {'user_form': user_form}
        )