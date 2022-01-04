from django.db.models.signals import pre_save, post_init, post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
from security.models import Security
from helpers.image import tnails


@receiver(post_save, sender=Security)
def save_photo_thumbnails(sender, instance, created, *args, **kwargs):
  if created:
    if instance.photo == 'null':
      instance.photo = None
    if instance.photo:
      photo, PHOTO_FTYPE, photo_thumb_filename = tnails(instance.photo)
      if photo is not None:
        temp_thumb = BytesIO()
        photo.save(temp_thumb, PHOTO_FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        instance.photo_thumbnail.save(photo_thumb_filename, ContentFile(
            temp_thumb.read()), save=False)
        temp_thumb.close()
  else:
    pass


@receiver(post_save, sender=Security)
def save_adharcard_thumbnails(sender, instance, created, *args, **kwargs):
  if created:
    if instance.adhar_card == 'null':
      instance.adhar_card = None
    if instance.adhar_card:
      adhar_card, ADHAR_FTYPE, adhar_card_thumb_filename = tnails(
          instance.adhar_card)
      if adhar_card is not None:
        temp_thumb = BytesIO()
        adhar_card.save(temp_thumb, ADHAR_FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        instance.adhar_card_thumbnail.save(adhar_card_thumb_filename, ContentFile(
            temp_thumb.read()), save=False)
        temp_thumb.close()
  else:
    pass
