from rest_framework import serializers
from fees.models import *


class FeesItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = FeesItem
    fields = (
      'id',
      'fields',
      'society'
    )

class PaymentSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)
  class Meta:
    model = Payment
    fields = (
      'id',
      'user',
      'full_name',
      'amount',
      'amount_break_up',
      'payment_month',
      'payment_year',
      'date',
      'status'
    )
