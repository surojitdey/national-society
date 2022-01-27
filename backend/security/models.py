from django.db import models
from django.utils.translation import ugettext_lazy as _

from society.models import Society


def security_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/security_documents/<id>/<filename>
    return '{0}/{1}/{2}'.format('security_documents', instance.full_name + str(instance.date_of_birth), filename)
def security_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/security_documents/<id>/<filename>
    return '{0}/{1}/{2}/{3}'.format('security_documents', instance.full_name + str(instance.date_of_birth), 'thumbnail', filename)


class Security(models.Model):
  class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')
  class Status(models.TextChoices):
    ACTIVE = 'active', _('active')
    DEACTIVE = 'deactive', _('deactive')
  
  society = models.ForeignKey(Society, on_delete=models.CASCADE, null=True)
  full_name = models.CharField(_('full name'), max_length=100, blank=False)
  father_name = models.CharField(_('father name'), max_length=100, blank=False)
  gender = models.CharField(_('gender'), choices=Gender.choices,
                              default=Gender.MALE, max_length=10, blank=False)
  added = models.DateTimeField(auto_now_add=True)
  date_of_joining = models.DateField(blank=False)
  permanent_address = models.TextField(_('permanent address'), max_length=500, blank=False)
  date_of_birth = models.DateField(blank=False)
  mobile_number = models.CharField(_('mobile number'), max_length=20)
  reference = models.CharField(_('reference'), max_length=100, blank=True)
  photo = models.FileField(upload_to=security_directory_path, blank=False)
  photo_thumbnail = models.FileField(
      upload_to=security_thumbnail_directory_path, blank=True)
  adhar_card = models.FileField(upload_to=security_directory_path, blank=False)
  adhar_card_thumbnail = models.FileField(
      upload_to=security_thumbnail_directory_path, blank=True)
  status = models.CharField(_('status'), choices=Status.choices,
                            default=Status.ACTIVE, max_length=10, blank=True)
  
  def __str__(self):
    return self.full_name


class Timetable(models.Model):
  class Day(models.TextChoices):
    ALL = 'all', _('all')
    MON = 'mon', _('mon')
    TUE = 'tue', _('tue')
    WED = 'wed', _('wed')
    THU = 'thu', _('thu')
    FRI = 'fri', _('fri')
    SAT = 'sat', _('sat')
    SUN = 'sun', _('sun')
  security = models.ForeignKey(
      Security, on_delete=models.CASCADE, related_name="security_timetable", to_field="id")
  task_date = models.DateField(blank=True, null=True)
  task_day = models.CharField(_('task day'), choices=Day.choices, default=Day.ALL, max_length=3, blank=False)
  start_time = models.TimeField(_('start time'), blank=False)
  end_time = models.TimeField(_('end time'), blank=False)

  def __str__(self):
    return self.task_date
