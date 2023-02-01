from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_users')
def index(request):
    return render(request, "app_addressbook/index.html", {'navbar': 'addressbook'})
