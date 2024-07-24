from django.shortcuts import render, redirect
from Users.models import CustomUser
from Users.forms import CustomUserRegisterForm, ProfileUpdateForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = CustomUserRegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'Users/register.html', context=context)

    def post(self, request):
        register_form = CustomUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Registration finished successfully')
            return redirect('users:login')
        else:
            context = {
                'register_form': register_form
            }
            return render(request, 'Users/register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        messages_to_display = messages.get_messages(request)
        context = {
            'login_form': login_form,
            'messages_to_display': messages_to_display
        }
        return render(request, 'Users/login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home:home')
        else:
            context = {
                'login_form': login_form
            }
            messages.error(request, 'Entered wrong login or password!')
        return render(request, 'Users/login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully')
        return redirect('home:home')


class ProfileView(View):
    def get(self, request):
        context = {
            'user': request.user
        }
        return render(request, 'Users/profile.html', context=context)


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        context = {
            'update_form': update_form
        }
        return render(request, 'Users/profile_update.html', context=context)

    def post(self, request):
        update_form = ProfileUpdateForm(data=request.POST, files=request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home:home')
        else:
            context = {
                'update_form': update_form
            }
            messages.error(request, 'Something went wrong')
            return render(request, 'Users/profile_update.html', context=context)





