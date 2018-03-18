from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


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
    #render(request, 'freshpointapp/index.html', {})
