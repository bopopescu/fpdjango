from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, FoodClass
from django.core.checks.security import csrf


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

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "upload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("upload"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split('\n')
        #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["UserID"] = fields[0]
            data_dict["ProductID"] = fields[1]
            data_dict["Size"] = fields[2]
            data_dict["Produce"] = fields[3]
            try:
                form = EventsForm(data_dict)
                if form.is_valid():
                    form.save()
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    
    return HttpResponseRedirect(reverse("upload"))

def intro(request):
    introduce = loader.get_template('freshpointapp/intro.html')
    context = {

    }
    return HttpResponse(introduce.render(context, request))


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
    return HttpResponse(logout.render(context, request))


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
