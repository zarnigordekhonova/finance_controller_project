from django.db import models
from django.conf import settings


class Accounts(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return f'{self.name}'


class TypeIncomes(models.Model):
    income_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'type_incomes'

    def __str__(self):
        return self.income_name


class TypeExpenditures(models.Model):
    expenditure_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'type_expenditures'

    def __str__(self):
        return self.expenditure_name


class Expenditures(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expenditure_type = models.ForeignKey(TypeExpenditures, on_delete=models.CASCADE)
    account_type = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'expenditures'

    def __str__(self):
        return f"{self.expenditure_type.expenditure_name} | {self.date} | {self.account_type.name}"


class Incomes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    income_type = models.ForeignKey(TypeIncomes, on_delete=models.CASCADE)
    account_type = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'incomes'

    def __str__(self):
        return f"{self.income_type.income_name} | {self.date} | {self.account_type.name}"
