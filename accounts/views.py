from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.validators import validate_email
from .models import UserAccount
from django.template import loader
from django.urls import reverse


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/index.html')

    username = request.POST.get('uname')
    password = request.POST.get('psw')

    user = get_object_or_404(UserAccount, username=username, password=password)
    try:
        avatar = user.avatar.url
    except:
        avatar = None

    if not user:
        return render(request, 'accounts/index.html')
    else:
        user_key = user.id
        request.session['user_key'] = user_key
        request.session['user'] = {
            'username': user.username,
            'name': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'phone': user.phone,
            'password': user.password,
            'avatar': avatar,
        }

        return redirect('home')


def logout(request):
    request.session = []
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    username = request.POST.get('username')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    psw = request.POST.get('psw')
    psw2 = request.POST.get('psw2')
    country = request.POST.get('country')
    # avatar = request.IMAGE['avatar']

    if not firstname or not lastname or not username or not phone or not email or not psw or not psw2 or not country:
        messages.error(request, 'No fields can be empty')
        return render(request, 'accounts/register.html')

    # Validador de email
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/register.html')

    # Validador de senha
    if len(psw) < 6:
        messages.error(request, 'Senha precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/register.html')

    if psw != psw2:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'accounts/register.html')

    # Verificação de usuario e email
    if UserAccount.objects.filter(username=username).exists():
        messages.error(request, 'Usuario já existe.')
        return render(request, 'accounts/register.html')

    if UserAccount.objects.filter(email=email).exists():
        messages.error(request, 'Email já cadastrado.  ')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso!')

    user = UserAccount()
    user.firstname = firstname
    user.lastname = lastname
    user.username = username
    user.phone = phone
    user.email = email
    user.password = psw
    user.country = country
    # user.avatar = avatar
    user.save()
    return HttpResponseRedirect(reverse('login'))


def profile(request):
    return render(request, 'accounts/profile.html')


def dados(request):
    usuarios = UserAccount.objects.all()
    return render(request, 'accounts/dados.html', {
        'usuarios': usuarios
    })
