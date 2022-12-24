from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login 

from .models import Player, NewPlayerForm

def accountView(request):
  if request.user.is_authenticated:
    return render(request, 'account/profile.html')
  return redirect('login')

def loginView(request):
  if request.user.is_authenticated:
    return redirect('account')
  errors = False
  if request.method == 'POST':
    login_form = AuthenticationForm(data=request.POST)
    if login_form.is_valid():
      login(request, login_form.get_user())
      return redirect('account')
    errors = True
  return render(request, 'account/login.html', { 'form': AuthenticationForm(), 'errors': errors})

def createAccountView(request):
  if request.user.is_authenticated:
    return redirect('account')
  errors = False
  if request.method == 'POST':
    user_form = NewPlayerForm(request.POST)
    if user_form.is_valid():
      new_player = user_form.save(commit=False)
      new_player.set_password(user_form.data['password'])
      new_player.save()
      return redirect('account')
    errors = True

  return render(request, 'account/create_account.html', { 'new_user_form': NewPlayerForm(), 'errors': errors})