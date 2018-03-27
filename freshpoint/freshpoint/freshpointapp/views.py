from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


class UserFormView(View):
    form_class = UserForm
    template_name = 'freshpointapp/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request)
                    return redirect('/success')

        # if user didn't login, redirect to login
        return render(request, self.template_name, {'form': form})


def intro(request):
    introduce = loader.get_template('freshpointapp/intro.html')
    context = {

    }
    return HttpResponse(introduce.render(context, request))


def about(request):
    about = loader.get_template('freshpointapp/about.html')
    context = {

    }
    return HttpResponse(about.render(context, request))


def index(request):
    mainpage = loader.get_template('freshpointapp/index.html')
    context = {

    }
    return HttpResponse(mainpage.render(context, request))


def login(request):
    login = loader.get_template('freshpointapp/login.html')
    context = {

    }
    return HttpResponse(login.render(context, request))


def logout(request):
    logout = loader.get_template('freshpointapp/logout.html')
    context = {

    }
    return redirect('login')


def success(request):
    success = loader.get_template('freshpointapp/success.html')
    context = {

    }
    return HttpResponse(success.render(context, request))


def upload(request):
    uploadpage = loader.get_template('freshpointapp/upload.html')
    context = {

    }
    return HttpResponse(uploadpage.render(context, request)) 
