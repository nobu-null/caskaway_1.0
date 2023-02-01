from app_finance.models import Sites


def extras(request):
    if 'admin' in request.META['PATH_INFO']:
        return {}
    elif request.user.is_authenticated:
        current_user = request.user
        site = Sites.objects.get(user_id=current_user)
        return {'site': site}
    else:
        return {}
