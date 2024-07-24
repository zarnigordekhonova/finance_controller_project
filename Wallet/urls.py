from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add_income/', views.AddIncomeView.as_view(), name='add_income'),
    path('add_expenditure/', views.AddExpenditureView.as_view(), name='add_expenditure'),
    path('expenditures/', views.ExpendituresListView.as_view(), name='expenditures'),
    path('incomes/', views.IncomesListView.as_view(), name='incomes'),
    path('edit_incomes/<int:pk>', views.EditIncomeView.as_view(), name='edit_incomes'),
    path('edit_expenditure/<int:pk>', views.EditExpenditureView.as_view(), name='edit_expenditure'),
    path('accounts_list/', views.AccountListView.as_view(), name='accounts_list'),
    path('add_accounts/', views.AddAccountView.as_view(), name='add_accounts'),
    path('delete_accounts/<int:pk>', views.DeleteAccount.as_view(), name='delete_accounts'),
    path('edit/<int:pk>/account/', views.EditAccountView.as_view(), name='edit_account')
]


