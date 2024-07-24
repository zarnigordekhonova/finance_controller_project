from django import forms
from .models import Incomes, Expenditures, Accounts


class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = Incomes
        fields = ['income_type', 'amount', 'date', 'description', 'account_type']
        widgets = {
            'income_type': forms.Select(attrs={'id': 'id_income_type'}),
            'amount': forms.NumberInput(attrs={'id': 'id_amount'}),
            'date': forms.DateInput(attrs={'id': 'id_date', 'type': 'date'}),
            'description': forms.Textarea(attrs={'id': 'id_description'}),
            'account_type': forms.Textarea(attrs={'id': 'account_type_id'}),
        }


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditures
        fields = ['expenditure_type', 'amount', 'date', 'description', 'account_type']
        widgets = {
            'expenditure_type': forms.Select(attrs={'id': 'id_expenditure_type'}),
            'amount': forms.NumberInput(attrs={'id': 'id_amount'}),
            'date': forms.DateInput(attrs={'id': 'id_date', 'type': 'date'}),
            'description': forms.Textarea(attrs={'id': 'id_description'}),
            'account_type': forms.Textarea(attrs={'id': 'account_type_id'}),
        }


class EditIncomeForm(forms.ModelForm):
    class Meta:
        model = Incomes
        fields = '__all__'


class EditExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditures
        fields = '__all__'


class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        exclude = ['user']


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = '__all__'

