from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic import TemplateView


def intro(request):
    introduce = loader.get_template('freshpointapp/intro.html')
    context = {

    }
    return HttpResponse(introduce.render(context, request))


def index(request):
    main = loader.get_template('freshpointapp/index.html')
    context = {

    }
    return HttpResponse(main.render(context, request))
