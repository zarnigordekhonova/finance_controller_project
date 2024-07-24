from django.contrib import admin
from Wallet.models import TypeIncomes, Incomes, Expenditures, Accounts, TypeExpenditures

# Register your models here.

admin.site.register(Accounts)
admin.site.register(TypeIncomes)
admin.site.register(TypeExpenditures)
admin.site.register(Expenditures)
admin.site.register(Incomes)