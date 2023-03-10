from django.db import models
from django.contrib.auth.models import User


class DateTable(models.Model):
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    day = models.TextField(db_column='Day', blank=True, null=True)  # Field name made lowercase.
    week = models.IntegerField(db_column='Week', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    quarter = models.IntegerField(db_column='Quarter', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'date_table'

    def __str__(self):
        return f'{self.date}'


class AgreementType(models.Model):
    type = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "agreement types"

    def __str__(self):
        return self.type


class PubGroup(models.Model):
    name = models.CharField(max_length=150)
    agreement = models.ForeignKey(AgreementType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "pub groups"

    def __str__(self):
        return f'{self.name} - {self.agreement}'


class Sites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(PubGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "sites"

    def __str__(self):
        return f'{self.name}'


class Epos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    wet = models.DecimalField(max_digits=10, decimal_places=2)
    dry = models.DecimalField(max_digits=10, decimal_places=2)
    pdq = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "epos"

    def __str__(self):
        return f'{self.site} - {self.date}'


class ExpensesCategory(models.Model):
    group = models.ForeignKey(PubGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "expense_categories"

    def __str__(self):
        return f'{self.name}'


class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    where = models.CharField(max_length=255)
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "expenses"

    def __str__(self):
        return f'{self.site} - {self.date} - {self.amount}'


class IncomeCategory(models.Model):
    group = models.ForeignKey(PubGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "income_categories"

    def __str__(self):
        return f'{self.name} - {self.group}'


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "income"

    def __str__(self):
        return f'{self.site} - {self.date} - {self.category} - {self.amount}'


class SafeCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    fifty_pound = models.IntegerField()
    twenty_pound = models.IntegerField()
    ten_pound = models.IntegerField()
    five_pound = models.IntegerField()
    one_pound = models.IntegerField()
    fifty_pence = models.DecimalField(max_digits=10, decimal_places=2)
    twenty_pence = models.DecimalField(max_digits=10, decimal_places=2)
    ten_pence = models.DecimalField(max_digits=10, decimal_places=2)
    five_pence = models.DecimalField(max_digits=10, decimal_places=2)
    coppers = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "safe_count"

    def __str__(self):
        return f'{self.site} - {self.date}'


class DepositsTaken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    who = models.CharField(max_length=255)
    notes = models.TextField()
    amount_in = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "deposits_taken"

    def __str__(self):
        return f'{self.who}'


class DepositsReturned(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    who = models.ForeignKey(DepositsTaken, on_delete=models.CASCADE)
    notes = models.TextField()
    amount_out = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "deposits_returned"

    def __str__(self):
        return f'{self.who}'


class Targets(models.Model):
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    collection = models.CharField(max_length=100)
    target = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "targets"

    def __str__(self):
        return f'{self.target}'


class Staff(models.Model):
    class Position(models.TextChoices):
        BAR_STAFF = 'BS', 'Bar Staff'
        BAR_BACK = 'BB', 'Bar Back'
        CLEANER = 'CL', 'Cleaner'
        ASSISTANT_MANAGER = 'AM', 'Assistant Manager'
        MANAGER = 'MA', 'Manager'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    position = models.CharField(max_length=2, choices=Position.choices, default=Position.BAR_STAFF,)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.position} - {self.salary}'


class HoursWorked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    staff_member = models.ForeignKey(Staff, on_delete=models.CASCADE)
    hours_worked = models.FloatField()
    wage = models.FloatField()

    class Meta:
        verbose_name_plural = "hours_worked"

    def __str__(self):
        return f'{self.staff_member} - {self.hours_worked}'


class CashHandover(models.Model):
    class Handover(models.TextChoices):
        IN_PERSON = 'IP', 'In Person'
        BANK = 'BK', 'Bank'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)
    date = models.ForeignKey(DateTable, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=Handover.choices, default=Handover.IN_PERSON,)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "cash_handover"

    def __str__(self):
        return f'{self.site} - {self.amount}'
