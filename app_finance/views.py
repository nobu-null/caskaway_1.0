from operator import attrgetter

from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import pandas as pd
import datetime
from decimal import *
from django.core.paginator import Paginator
from itertools import chain
from django.template import loader
from app_finance.forms import EposForm, ExpensesForm, IncomeForm, DepositTakenForm, DepositReturnedForm, SafeCountForm, \
                   HoursWorkedForm, StaffForm, CashHandoverForm
from app_finance.models import Sites, Epos, Expenses, ExpensesCategory, IncomeCategory, Targets, DateTable, \
                    HoursWorked, DepositsTaken, DepositsReturned, Income, SafeCount, Staff, CashHandover


def is_num(number):
    if number is None:
        return 0
    else:
        return number


@login_required(login_url='login_users')
def index(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk

    epos = Epos.objects.filter(user_id=user).aggregate(sum=Sum('wet') + Sum('dry'))
    expenses = Expenses.objects.filter(user_id=user).aggregate(sum=Sum('amount'))
    income = Income.objects.filter(user_id=user).aggregate(sum=Sum('amount'))

    cashhandover = CashHandover.objects.filter(user_id=user).aggregate(sum=Sum('amount'))
    deposits_taken = DepositsTaken.objects.filter(user_id=user).aggregate(sum=Sum('amount_in'))
    deposits_returned = DepositsReturned.objects.filter(user_id=user).aggregate(sum=Sum('amount_out'))

    wages = HoursWorked.objects.filter(user_id=user).aggregate(sum=Sum('wage'))

    safe = SafeCount.objects.filter(user_id=user).aggregate(sum=Sum('fifty_pound') + Sum('twenty_pound') +
                                Sum('ten_pound') + Sum('five_pound') + Sum('one_pound') + Sum('fifty_pence')
                                + Sum('twenty_pence') + Sum('ten_pence') + Sum('five_pence') + Sum('coppers'))

    sum_epos = epos['sum']
    sum_income = income['sum']
    sum_expenses = expenses['sum']
    deposit_in = deposits_taken['sum']
    deposit_out = deposits_returned['sum']
    wage = wages['sum']
    insafe = safe['sum']
    handover = cashhandover['sum']

    cashonsite = is_num(insafe) - is_num(handover)

    revenue = (is_num(sum_epos) + is_num(sum_income))
    percentage = (Decimal(27) * revenue) / Decimal(100.00)
    balance = is_num(percentage) - (is_num(sum_expenses) + Decimal(is_num(wage)))
    deposit_account = is_num(deposit_in) - is_num(deposit_out)

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
        form = DepositTakenForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_depositReturned' in request.POST:
        form = DepositReturnedForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_hours' in request.POST:
        form = HoursWorkedForm(request.POST)
        date = request.POST.get('dateSelect')
        staff = request.POST.get('staff_member')
        hours = request.POST.get('hours_worked')
        salary = Staff.objects.filter(id=staff).values_list('salary', flat=True)
        s = Decimal(salary[0])
        h = Decimal(hours)
        wage = h * s
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.wage = wage
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

    if 'save_staff' in request.POST:
        form = StaffForm(request.POST)
        date = request.POST.get('dateSelect')
        if form.is_valid():
            x = form.save(commit=False)
            x.site_id = site
            x.user_id = user
            x.date_id = date
            x.save()
            return HttpResponseRedirect('/finance/')

    if 'save_handover' in request.POST:
        form = CashHandoverForm(request.POST)
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

        deposittaken = DepositTakenForm()
        depositreturned = DepositReturnedForm()

        safeform = SafeCountForm
        staffform = StaffForm
        cashhandover = CashHandoverForm

        hoursworked = HoursWorkedForm

    context = {
        'eposform': eposform,
        'expensesform': expensesform,
        'incomeform': incomeform,
        'hoursworked': hoursworked,
        'depositform': deposittaken,
        'depositreturned': depositreturned,
        'safeform': safeform,
        'staffform': staffform,
        'cashhandover': cashhandover,
        'navbar': 'finance',
        'revenue': revenue,
        'expenses': expenses,
        'balance': balance,
        'income': income,
        'cashonsite': cashonsite,
        'wage': wage,
        'deposits': deposit_account,
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
def epos_summary(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk
    p = Paginator(Epos.objects.filter(site_id=site).order_by('-date'), 5)
    page = request.GET.get('page')
    epos_pages = p.get_page(page)
    context = {
        'epos_pages': epos_pages,
        'navbar': 'summary',
    }
    return render(request, "app_finance/epos_summary.html", context)


@login_required(login_url='login_users')
def income_summary(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk
    p = Paginator(Income.objects.filter(site_id=site).order_by('-date'), 5)
    page = request.GET.get('page')
    income_pages = p.get_page(page)
    context = {
        'income_pages': income_pages,
        'navbar': 'summary',
    }
    return render(request, "app_finance/income_summary.html", context)

@login_required(login_url='login_users')
def expenses_summary(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk
    p = Paginator(Expenses.objects.filter(site_id=site).order_by('-date'), 5)
    page = request.GET.get('page')
    expenses_pages = p.get_page(page)
    context = {
        'expenses_pages': expenses_pages,
        'navbar': 'summary',
    }
    return render(request, "app_finance/expenses_summary.html", context)

@login_required(login_url='login_users')
def deposits_summary(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk
    q1 = DepositsTaken.objects.filter(site_id=site)
    q2 = DepositsReturned.objects.filter(site_id=site)
    query = list(chain(q1, q2))
    q = sorted(query, key=lambda x: x.id)
    p = Paginator(q, 5)
    page = request.GET.get('page')
    deposits_pages = p.get_page(page)
    context = {
        'deposits_pages': deposits_pages,
        'navbar': 'summary',
    }
    return render(request, "app_finance/deposits_summary.html", context)

@login_required(login_url='login_users')
def hours_summary(request):
    user = request.user.pk
    site = Sites.objects.get(user_id=user).pk
    p = Paginator(HoursWorked.objects.filter(site_id=site).order_by('-date'), 5)
    page = request.GET.get('page')
    hours_pages = p.get_page(page)
    context = {
        'hours_pages': hours_pages,
        'navbar': 'summary',
    }
    return render(request, "app_finance/hours_summary.html", context)


@login_required(login_url='login_users')
def update_epos(request, id):
    epos = Epos.objects.get(id=id)
    form = EposForm(request.POST or None, instance=epos)
    if form.is_valid():
        form.save()
        return redirect('epos-summary')
    context = {
        'epos': epos,
        'form': form
    }
    return render(request, 'app_finance/update_epos.html', context)
