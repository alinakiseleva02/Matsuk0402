from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    else:
        context['login_form'] = CustomLoginForm()
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт успешно создан для {username}! Теперь вы можете войти.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')