from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm


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
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})