from random import shuffle
import random
import math
from django.db import models
from django.utils.translation import ugettext_lazy as _


def generate_random_number():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    random_number = ""

   # length of password can be chaged
   # by changing value in range
    for i in range(2):
        random_number += digits[math.floor(random.random() * 10)]

    return random_number

def shuffle_word(word):
  word = list(word)
  shuffle(word)
  return ''.join(word)

def generate_registration_number(society_name):
  char_string = ''.join(society_name[:3].upper() + generate_random_number())
  return shuffle_word(char_string)


class Society(models.Model):
  mobile_number = models.CharField(
      _('mobile number'), max_length=20, unique=True)
  society_name = models.CharField(_('full name'), max_length=100, blank=False)
  address = models.TextField(_('address'), max_length=500, blank=False)
  city = models.CharField(_('city'), max_length=50, blank=False)
  pincode = models.CharField(_('pincode'), max_length=50, blank=False)
  country = models.CharField(_('country'), max_length=50, blank=False)
  date_of_join = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(
      _('is active'), default=True, blank=True)
  email = models.EmailField(_('email'), max_length=254, blank=True, null=True)
  registration_number = models.CharField(
      _('registration number'), max_length=50, default='', unique=True)

  def save(self, *args, **kwargs):
    self.registration_number = generate_registration_number(self.society_name)
    super(Society, self).save(*args, **kwargs)

  def __str__(self):
    return self.society_name
