from django.shortcuts import render, redirect, get_object_or_404
from Wallet.models import Incomes, Expenditures, Accounts, TypeIncomes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from Wallet.forms import (AddIncomeForm, ExpenditureForm, EditIncomeForm,
                          EditExpenditureForm, AddAccountForm, EditAccountForm)
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.timezone import now
from collections import defaultdict
from decimal import Decimal



class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        total_income = Incomes.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenditure = Expenditures.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_sum = total_income-total_expenditure

        context = {
            'total_income': total_income,
            'total_expenditure': total_expenditure,
            'total_sum': total_sum
        }

        return render(request, 'Wallet/dashboard.html', context=context)


class AddIncomeView(LoginRequiredMixin, View):
    def get(self, request):
        income_form = AddIncomeForm()
        context = {
            'income_form': income_form
        }
        return render(request, 'Wallet/add_income.html', context=context)

    def post(self, request):
        income_form = AddIncomeForm(data=request.POST)
        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.user = request.user
            income.date = timezone.now().date()

            if income_form.cleaned_data['income_type'] == 'other':
                other_income_type_name = income_form.cleaned_data['other_income_type']
                income_type, created = TypeIncomes.objects.get_or_create(name=other_income_type_name)
                income.income_type = income_type
            else:
                income.income_type = income_form.cleaned_data['income_type']

            income.save()
            return redirect('wallet:incomes')
        else:
            print(income_form.errors)
            return self.get(request)


class AddExpenditureView(LoginRequiredMixin, View):
    def get(self, request):
        expenditure_form = ExpenditureForm()
        context = {
            'expenditure_form': expenditure_form
        }
        return render(request, 'Wallet/add_expenditure.html', context=context)

    def post(self, request):
        expenditure_form = ExpenditureForm(data=request.POST)
        if expenditure_form.is_valid():
            expenditure = expenditure_form.save(commit=False)
            expenditure.user = request.user
            expenditure.date = datetime.now().date().isoformat()
            expenditure.save()
            return redirect('wallet:expenditures')
        else:
            context = {
                'expenditure_form': expenditure_form
            }
        return render(request, 'Wallet/add_expenditure.html', context)


class ExpendituresListView(View):
    def get(self, request):
        filter_date = request.GET.get('date', None)
        filter_period = request.GET.get('period', 'daily')

        if filter_date:
            selected_date = parse_date(filter_date)
        else:
            selected_date = now().date()

        if filter_period == 'weekly':
            start_date = selected_date - timedelta(days=selected_date.weekday())
            end_date = selected_date + timedelta(days=6)
        elif filter_period == 'monthly':
            start_date = selected_date.replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        else:
            start_date = selected_date
            end_date = selected_date

        filtered_expenditures = Expenditures.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('-date')

        total_income = Incomes.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenditure = Expenditures.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_sum = total_income - total_expenditure

        expenditure_sum = filtered_expenditures.aggregate(Sum('amount'))['amount__sum'] or 0
        expenditure_type_totals = defaultdict(Decimal)
        for expenditure in filtered_expenditures:
            expenditure_type_totals[expenditure.expenditure_type.expenditure_name] += expenditure.amount

        expenditure_type_percentages = {
            k: {'amount': float(v), 'percentage': float(v) / float(expenditure_sum) * 100 if expenditure_sum else 0}
            for k, v in expenditure_type_totals.items()
        }

        context = {
            'total_income': total_income,
            'total_expenditure': total_expenditure,
            'total_sum': total_sum,
            'filter_date': filter_date,
            'filtered_expenditures': filtered_expenditures,
            'selected_date': selected_date,
            'start_date': start_date,
            'end_date': end_date,
            'filter_period': filter_period,
            'expenditure_sum': float(expenditure_sum),
            'expenditure_type_percentages': expenditure_type_percentages
        }
        return render(request, 'Wallet/expenses.html', context)


class IncomesListView(View):
    def get(self, request):
        filter_date = request.GET.get('date', None)
        filter_period = request.GET.get('period', 'daily')

        if filter_date:
            selected_date = parse_date(filter_date)
        else:
            selected_date = now().date()

        if filter_period == 'weekly':
            start_date = selected_date - timedelta(days=selected_date.weekday())
            end_date = start_date + timedelta(days=6)
        elif filter_period == 'monthly':
            start_date = selected_date.replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        else:
            start_date = selected_date
            end_date = selected_date

        filtered_incomes = Incomes.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('-date')

        total_income = Incomes.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenditure = Expenditures.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_sum = total_income - total_expenditure

        income_sum = filtered_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        income_type_totals = defaultdict(Decimal)
        for income in filtered_incomes:
            income_type_totals[income.income_type.income_name] += income.amount

        income_type_percentages = {
            k: {'amount': float(v), 'percentage': (float(v) / float(income_sum) * 100) if income_sum else 0}
            for k, v in income_type_totals.items()
        }

        context = {
            'filtered_incomes': filtered_incomes,
            'total_amount': total_income,
            'total_expenditure': total_expenditure,
            'total_sum': total_sum,
            'selected_date': selected_date,
            'start_date': start_date,
            'end_date': end_date,
            'filter_period': filter_period,
            'income_sum': float(income_sum),
            'income_type_percentages': income_type_percentages,
        }
        return render(request, 'Wallet/incomes.html', context)


class EditIncomeView(View):
    def get(self, request, pk):
        income = get_object_or_404(Incomes, pk=pk)
        edit_income_form = EditIncomeForm(instance=income)
        context = {
            'income': income,
            'edit_income_form': edit_income_form
        }
        return render(request, 'Wallet/edit_income.html', context=context)

    def post(self, request, pk):
        incomes = get_object_or_404(Incomes, pk=pk)
        edit_income_form = EditIncomeForm(request.POST, instance=incomes)
        if edit_income_form.is_valid():
            edit_income_form.save()
            messages.success(request, 'Your income data has been updated successfully.')
            return redirect('wallet:incomes')
        else:
            context = {
                'incomes': incomes,
                'edit_income_form': edit_income_form
            }
            return render(request, 'Wallet/edit_income.html', context=context)


class EditExpenditureView(View):
    def get(self, request, pk):
        expenditures = get_object_or_404(Expenditures, pk=pk)
        edit_expenditure_form = EditExpenditureForm(instance=expenditures)
        context = {
            'expenditures': expenditures,
            'edit_expenditure_form': edit_expenditure_form
        }
        return render(request, 'Wallet/edit_expenditure.html', context=context)

    def post(self, request, pk):
        expenditures = get_object_or_404(Expenditures, pk=pk)
        edit_expenditure_form = EditExpenditureForm(request.POST, instance=expenditures)
        if edit_expenditure_form.is_valid():
            edit_expenditure_form.save()
            messages.success(request, 'Your expenditure data has been updated successfully.')
            return redirect('wallet:expenditures')
        else:
            context = {
                'expenditures': expenditures,
                "edit_expenditure_form": edit_expenditure_form
            }
            return render(request, 'Wallet/edit_expenditure.html', context=context)


class AccountListView(View, LoginRequiredMixin):
    def get(self, request):
        account = Accounts.objects.filter(user=request.user)
        context = {
            'account': account
        }
        return render(request, 'Wallet/account_list.html', context=context)


class AddAccountView(LoginRequiredMixin, View):
    def get(self, request):
        account_form = AddAccountForm()
        context = {
            'account_form': account_form
        }
        return render(request, 'Wallet/add_account.html', context=context)

    def post(self, request):
        account_form = AddAccountForm(data=request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.save()
            return redirect('wallet:accounts_list')
        else:
            context = {
                'account_form': account_form
            }
            return render(request, 'Wallet/add_account.html', context=context)



class DeleteAccount(LoginRequiredMixin, View):
    def post(self, request, pk):
        account = get_object_or_404(Accounts, pk=pk)
        if account.user == request.user:
            account.delete()
            messages.success(request, 'Account deleted successfully.')
            return redirect('wallet:accounts_list')
        else:
            messages.error(request, 'You do not have permission to delete this account.')
            return redirect('wallet:accounts_list')


class EditAccountView(View):
    def get(self, request, pk):
        accounts = get_object_or_404(Accounts, pk=pk)
        account_form = EditAccountForm(instance=accounts)

        context = {
            'accounts': accounts,
            'account_form': account_form
        }
        return render(request, 'Wallet/edit_account.html', context=context)

    def post(self, request, pk):
        accounts = get_object_or_404(Accounts, pk=pk)
        account_form = EditAccountForm(data=request.POST, instance=accounts)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, 'Your account data has been updated successfully.')
            return redirect('wallet:accounts_list')
        else:
            context = {
                'accounts': accounts,
                'account_form': account_form
            }
            return render(request, 'Wallet/edit_account.html', context=context)

