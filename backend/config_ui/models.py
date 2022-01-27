from django.db import models
from django.utils.translation import ugettext_lazy as _

from society.models import Society


class SettingDetails(models.Model):
  society = models.ForeignKey(Society, on_delete=models.CASCADE, null=True)
  community_name = models.CharField(
      _('community name'), max_length=100, blank=True)
  appartment_name = models.CharField(
      _('appartment name'), max_length=100, blank=True)
  address_one = models.CharField(
      _('address one'), max_length=200, blank=True)
  address_two = models.CharField(
      _('address two'), max_length=200, blank=True)
  city = models.CharField(_('city'), max_length=200, blank=True)
  pincode = models.CharField(_('pincode'), max_length=6, blank=True)
  contact_number = models.CharField(_('contact number'), max_length=13, blank=True)
  email = models.EmailField(_('email address'), blank=True)
  show_address = models.BooleanField(_('show address'), default=True, blank=True)
  show_number = models.BooleanField(_('show contact number'), default=True, blank=True)
  show_email = models.BooleanField(_('show email-id'), default=True, blank=True)
  enable_events = models.BooleanField(_('enable events'), default=True, blank=True)
  enable_news = models.BooleanField(_('enable news'), default=True, blank=True)
  enable_posts = models.BooleanField(_('enable posts'), default=True, blank=True)
  show_complaints = models.BooleanField(_('show complaints'), default=True, blank=True)
