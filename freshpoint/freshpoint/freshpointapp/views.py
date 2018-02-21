from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    template = loader.get_template('freshpointapp/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))
