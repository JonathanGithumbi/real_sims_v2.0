from django.db import models


class Expense(models.Model):
    class Meta:
        permissions = [
            ("can_create_an_expense", "can create an expense"),
            ("can_edit_an_expense", "can edit and expense"),
            ("can_view_expenses", "can view expenses"),
            ("can_delete_an_expense", "can discard and expense"),
            ("can_confirm_add_an_expense", "can confirm add and expense"),
            ("can_view_summaries", "can view summaries")
        ]

    EXPENSE_CATEGORIES = [
        ("petty cash", "petty cash"),
        ("school transport", "school transport"),
        ("electricity", "electricity"),
        ("water", "water"),
        ("payroll", "payroll"),
        ("taxes", "taxes"),
        ("other", "other")
    ]
    recipient = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=EXPENSE_CATEGORIES)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_per_quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    synced = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    qb_id = models.CharField(max_length=255, null=True, default=None)
    fully_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.description
