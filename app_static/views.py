from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_finance.models import Sites


@login_required(login_url='login_users')
def index(request):
    current_user = request.user
    site = Sites.objects.get(user_id=current_user)
    context = {
        "user": current_user,
        "site": site,
    }
    return render(request, "app_static/index.html", context)
