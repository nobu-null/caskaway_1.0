from django import forms
from .models import Epos, Expenses, Income, Deposits, Orders, SafeCount, DateTable
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'



class EposForm(forms.ModelForm):

    class Meta:
        model = Epos
        fields = ['wet', 'dry', 'pdq']
        widgets = {
            'wet': forms.NumberInput(attrs={'class': 'form-control validate-number', 'id': 'f3', 'value': '0',
                                            'onClick': 'this.select();'}),
            'dry': forms.NumberInput(attrs={'class': 'form-control validate-number', 'id': 'f3', 'value': '0',
                                            'onClick': 'this.select();'}),
            'pdq': forms.NumberInput(attrs={'class': 'form-control validate-number', 'id': 'f3', 'value': '0',
                                            'onClick': 'this.select();'}),
        }


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['where', 'category', 'item', 'amount']
        widgets = {
            'where': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Please Select'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'description', 'amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposits
        fields = ['who', 'category', 'amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'who': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['category',  'amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SafeCountForm(forms.ModelForm):
    class Meta:
        model = SafeCount
        fields = ['fifty_pound', 'twenty_pound', 'ten_pound', 'five_pound', 'one_pound',
                  'fifty_pence', 'twenty_pence', 'ten_pence', 'five_pence', 'coppers' ]
        widgets = {
            'fifty_pound': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'twenty_pound': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'ten_pound': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'five_pound': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'one_pound': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'fifty_pence': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'twenty_pence': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'ten_pence': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'five_pence': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
            'coppers': forms.NumberInput(attrs={'class': 'form-control', 'value': '0', 'onClick': 'this.select();'}),
        }
