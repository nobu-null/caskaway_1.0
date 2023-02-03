from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import EposForm, ExpensesForm, IncomeForm, DepositForm, OrderForm, SafeCountForm, HoursWorkedForm
from django.http import HttpResponseRedirect
from .models import Sites, Epos, Expenses, ExpensesCategory, IncomeCategory, DepositCategory, OrderCategory, Deposits, Targets, DateTable, HoursWorked
from django.db.models import Sum
import pandas as pd
import datetime


@login_required(login_url='login_users')
def index(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk

    income = Epos.objects.filter(user_id=user).aggregate(sum=Sum('wet') + Sum('dry'))
    expenses = Expenses.objects.filter(user_id=user).aggregate(sum=Sum('amount'))
    i = income['sum']
    e = expenses['sum']
    deposits = Deposits.objects.filter(user_id=user).aggregate(sum=Sum('amount'))

    if i is None and e is None:
        balance = 0
    elif e is None:
        balance = i - 0
    elif i is None:
        balance = 0 - e
    else:
        balance = i - e

    todays_date = datetime.date.today()
    week = todays_date.isocalendar().week
    year = todays_date.isocalendar().year
    this_week = DateTable.objects.filter(week=week, year=year)

    if 'save_epos' in request.POST:
        form = EposForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_expenses' in request.POST:
        form = ExpensesForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_income' in request.POST:
        form = IncomeForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_deposit' in request.POST:
        form = DepositForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_hours' in request.POST:
        form = HoursWorked(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_safe' in request.POST:
        form = SafeCountForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    else:

        eposform = EposForm

        expensesform = ExpensesForm()
        expensesform.fields["category"].queryset = ExpensesCategory.objects.filter(group_id=site)

        incomeform = IncomeForm()
        incomeform.fields["category"].queryset = IncomeCategory.objects.filter(group_id=site)

        depositform = DepositForm()
        depositform.fields["category"].queryset = DepositCategory.objects.filter(group_id=site)

        orderform = OrderForm()
        orderform.fields["category"].queryset = OrderCategory.objects.filter(group_id=site)

        safeform = SafeCountForm

        hoursworked = HoursWorkedForm


    context = {
        'eposform': eposform,
        'expensesform': expensesform,
        'incomeform': incomeform,
        'hoursworked': hoursworked,
        'depositform': depositform,
        'safeform': safeform,
        'navbar': 'finance',
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'deposits': deposits,
        'this_week': this_week,



    }
    return render(request, "app_finance/index.html", context)


@login_required(login_url='login_users')
def targets(request):

    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk

    w1 = Epos.objects.filter(date__week=1, site_id=site).aggregate(actual=Sum('wet') + Sum('dry'))
    t1 = Targets.objects.filter(collection='1', site_id=site).aggregate(target=Sum('target'))

    w2 = Epos.objects.filter(date__week=2, site_id=site).aggregate(actual=Sum('wet') + Sum('dry'))
    t2 = Targets.objects.filter(collection='2', site_id=site).aggregate(target=Sum('target'))

    w3 = Epos.objects.filter(date__week=3, site_id=site).aggregate(actual=Sum('wet') + Sum('dry'))
    t3 = Targets.objects.filter(collection='3', site_id=site).aggregate(target=Sum('target'))

    context = {
        'navbar': 'targets',
        'w1': w1,
        't1': t1,
        'w2': w2,
        't2': t2,
        'w3': w3,
        't3': t3,
    }
    return render(request, "app_finance/targets.html", context)


@login_required(login_url='login_users')
def summary(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk

    epos_df = pd.DataFrame(Epos.objects.filter(site_id=site).values()).drop(['id', 'user_id', 'site_id'], axis=1)
    expenses_df = pd.DataFrame(Expenses.objects.filter(site_id=site).values()).drop(['id', 'user_id', 'category_id', 'site_id'],
                                                                                    axis=1)


    context = {
        'navbar': 'summary',

        'epos': epos_df.to_html(classes='table bg-dark-light', border=0, index=False, justify='left'),
        'expenses': expenses_df.to_html(classes='table bg-dark-light', border=0, index=False, justify='left'),
    }
    return render(request, "app_finance/summary.html", context)
