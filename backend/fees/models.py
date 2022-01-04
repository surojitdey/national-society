from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User

class FeesItem(models.Model):
  fields = models.JSONField()

class Payment(models.Model):
  class Status(models.TextChoices):
    PAID = 'paid', _('paid')
    UNPAID = 'unpaid', _('unpaid')

  user = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name="payment_user", to_field="id")
  amount = models.CharField(_('amount'), max_length=100, blank=True)
  amount_break_up = models.JSONField()
  payment_month = models.CharField(_('payment month'), max_length=100, blank=True)
  payment_year = models.CharField(_('payment year'), max_length=100, blank=True)
  date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(_('payment status'), max_length=15,
                          choices=Status.choices, default=Status.UNPAID, blank=True)
