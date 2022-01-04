from rest_framework import serializers
from security.models import Security, Timetable


class SecuritySerializer(serializers.ModelSerializer):
  class Meta:
    model = Security
    fields = (
      'id',
      'full_name',
      'father_name',
      'gender',
      'added',
      'date_of_joining',
      'permanent_address',
      'date_of_birth',
      'mobile_number',
      'reference',
      'photo',
      'photo_thumbnail',
      'adhar_card',
      'adhar_card_thumbnail',
      'status'
    )


class UpdateSecuritySerializer(serializers.Serializer):
  security_id = serializers.CharField(max_length=20)
  full_name = serializers.CharField(max_length=100)
  father_name = serializers.CharField(max_length=2000)
  gender = serializers.CharField(max_length=2000)
  date_of_joining = serializers.DateField()
  permanent_address = serializers.CharField(max_length=2000)
  date_of_birth = serializers.DateField()
  mobile_number = serializers.CharField(max_length=2000)
  reference = serializers.CharField(max_length=2000)
  # media_file = serializers.FileField()


class UpdateStatusSerializer(serializers.Serializer):
  status = serializers.CharField(max_length=20)
  security_id = serializers.CharField(max_length=20)


class SetTimetableSerializer(serializers.ModelSerializer):
  class Meta:
    model = Timetable
    fields = (
      'id',
      'security',
      'task_date',
      'task_day',
      'start_time',
      'end_time'
    )


class GetTimetableSerializer(serializers.ModelSerializer):
  security = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='security.full_name', read_only=True)
  class Meta:
    model = Timetable
    fields = (
      'id',
      'security',
      'task_date',
      'task_day',
      'start_time',
      'end_time',
      'full_name'
    )


class DeleteTimeSerializer(serializers.Serializer):
  id = serializers.CharField(max_length=20)
