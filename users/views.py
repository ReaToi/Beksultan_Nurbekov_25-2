from users.forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView, DetailView, DeleteView


# Create your views here.


class RegisterCVB(ListView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            context = {
                'form': RegisterForm,

            }
            return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = RegisterForm(data=data)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                return redirect('/users/login/')

            else:
                form.add_error('password1', 'Password mismatch')

        return render(request, self.template_name, context={
            'form': form
        })


class LoginViewCBV(ListView, CreateView):
    def get(self, request, *args, **kwargs):
        context = {
            'form': LoginForm
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = LoginForm(data=data)
        if form.is_valid():
            """ authenticate """
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user:
                """ authorzation """
                login(request, user)
                return redirect('/products')
            else:
                form.add_error('username', 'User not found')

        return render(request, self.template_name, context={
            'form': form
        })


class LogoutViewCBV(ListView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/products/')


