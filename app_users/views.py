from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('financeHome')
        else:
            messages.add_message(request, messages.ERROR, "There was an error loging in, please try again")
            return redirect('login_users')

    else:
        return render(request, 'authentication/login.html', {})


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, "You've been Logged Out")
    return redirect('login_users')

