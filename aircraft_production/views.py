from django.shortcuts import render

from environs import Env

env = Env()
env.read_env(
    override=True
)


def login_view(request):
    context = {
        'client_id': env.str('CLIENT_ID_TOKEN'),
        'client_secret': env.str('CLIENT_SECRET_TOKEN'),
        'token_url': env.str('TOKEN_URL')
    }
    return render(request, 'login.html', context)


def home(request):
    context = {
        'token_url': env.str('TOKEN_URL')
    }
    return render(request, 'home.html', context)


def inventories(request):
    return render(request, 'inventories.html')


def stocks(request):
    return render(request, 'stocks.html')


def managers(request):
    return render(request, 'managers.html')
