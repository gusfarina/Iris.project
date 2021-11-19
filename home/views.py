from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home(request):
    try:
        is_logged = request.session['is_logged']
    except KeyError as err:
        return render(request, 'accounts/index.html')

    template_name = 'home/home.html'
    template = loader.get_template(template_name)
    context = {
        'page_title': 'Home',
    }
    return HttpResponse(template.render(context, request))


def about(request):
    try:
        is_logged = request.session['is_logged']
    except KeyError as err:
        return render(request, 'accounts/index.html')

    template_name = 'home/about.html'
    template = loader.get_template(template_name)
    context = {
        'page_title': 'About',
    }
    return HttpResponse(template.render(context, request))


def contact(request):
    try:
        is_logged = request.session['is_logged']
    except KeyError as err:
        return render(request, 'accounts/index.html')

    template_name = 'home/contact.html'
    template = loader.get_template(template_name)
    context = {
        'page_title': 'Contact',
    }
    return HttpResponse(template.render(context, request))


def team(request):
    try:
        is_logged = request.session['is_logged']
    except KeyError as err:
        return render(request, 'accounts/index.html')

    template_name = 'home/team.html'
    template = loader.get_template(template_name)
    context = {
        'page_title': 'Team',
    }
    return HttpResponse(template.render(context, request))
