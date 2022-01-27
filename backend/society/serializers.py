from rest_framework import serializers
from society.models import Society


class SocietySerializer(serializers.ModelSerializer):
  class Meta:
    model = Society
    fields = (
        'id',
        'mobile_number',
        'society_name',
        'address',
        'city',
        'pincode',
        'country',
        'email',
        'date_of_join',
        'is_active',
        'registration_number'
    )


class RegistrationValiditySerializer(serializers.Serializer):
  society_registration_number = serializers.CharField(max_length=50)
