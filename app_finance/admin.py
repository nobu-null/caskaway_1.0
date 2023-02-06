from django.contrib import admin
from django.apps import apps
from .models import Sites, PubGroup, AgreementType, Epos, Expenses, ExpensesCategory, \
    IncomeCategory, Targets, Staff, DepositsTaken, DepositsReturned


@admin.register(Sites)
class SitesAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "group")


@admin.register(PubGroup)
class SitesAdmin(admin.ModelAdmin):
    list_display = ("name", "agreement")


@admin.register(AgreementType)
class SitesAdmin(admin.ModelAdmin):
  pass


@admin.register(Epos)
class EposAdmin(admin.ModelAdmin):
  pass


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ("site", "category", "amount")


@admin.register(ExpensesCategory)
class ExpensesCategoryAdmin(admin.ModelAdmin):
  pass


@admin.register(IncomeCategory)
class ExpensesCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group")


@admin.register(Targets)
class TargetsAdmin(admin.ModelAdmin):
    list_display = ("site", "collection")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(DepositsTaken)
class DepositsTakenAdmin(admin.ModelAdmin):
    list_display = ("who", "amount_in")


@admin.register(DepositsReturned)
class DepositsReturnedAdmin(admin.ModelAdmin):
    list_display = ("who", "amount_out")

