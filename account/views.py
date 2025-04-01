from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('randomizer:index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # If it's an htmx request, send an HX-Redirect header.
            if request.headers.get('HX-Request'):
                response = JsonResponse({'success': True})
                response['HX-Redirect'] = reverse('randomizer:index')
                return response
            return redirect('randomizer:index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'account/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('randomizer:index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('randomizer:index')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('account:login')
