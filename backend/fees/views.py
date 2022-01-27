from django.shortcuts import render
from datetime import datetime, date
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from users.models import User
from fees.models import *
from fees.serializers import *
from service_auth.permissions import IsAdminUser, IsUser, IsUserReadOnly
from helpers.business import users_payment_data, get_user_due_months, get_modified_payment_details, adjust_date_and_months, users_paid_payment_data
from helpers.pagination import StandardResultsSetPagination


class FeesItemViewset(viewsets.ModelViewSet):
  queryset = FeesItem.objects.all()
  serializer_class = FeesItemSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'GET':
      self.permission_classes = [IsAdminUser | IsUser]
    return super(FeesItemViewset, self).get_permissions()
  
  def get_queryset(self):
    return FeesItem.objects.filter(society=self.request.user.society)

  def perform_create(self, serializer):
    serializer.save(society=self.request.user.society)


class UpdateFeesItemViewset(viewsets.ModelViewSet):
  queryset = FeesItem.objects.all()
  serializer_class = FeesItemSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    try:
      fees_items = FeesItem.objects.get(id=self.request.data.get('id'), society=self.request.user.society)
      fees_items.fields = self.request.data.get('fields')
      fees_items.save()
      return Response({
        'status': True,
        'details': 'Fees items are updated' 
      }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
      return Response({
        'status': False,
        'details': 'Fees items are not found'
      }, status=status.HTTP_404_NOT_FOUND)


class PaymentViewset(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'GET':
      self.permission_classes = [IsAdminUser | IsUser]
    return super(PaymentViewset, self).get_permissions()

  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    if(serializer.is_valid()):
      try:
        payment = Payment.objects.get(id=self.request.data.get('id'), user__society=self.request.user.society)
        if payment:
          payment.status = self.request.data.get('status')
          payment.save()
          return Response({
            'status': True,
            'details': 'Payment is updated.'
          }, status=status.HTTP_200_OK)
        else:
          return Response({
            'status': False,
            'details': 'Payment is not found.'
          }, status=status.HTTP_200_OK)
      except ObjectDoesNotExist:
        return Response({
          'status': False,
          'details': 'Payment does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPaymentStatusViewset(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsAdminUser]
  
  def list(self, request):
    from_month, from_year = self.request.query_params.get(
        'from_month'), self.request.query_params.get('from_year')
    to_month, to_year = self.request.query_params.get(
        'to_month'), self.request.query_params.get('to_year')
    from_month, to_month, from_year, to_year = adjust_date_and_months(
        from_month, to_month, from_year, to_year)

    user_data = users_payment_data(self.request.query_params.get('user'), from_month, from_year, to_month, to_year)
    serializer = self.serializer_class(user_data, many=True)

    new_serializer_data = serializer.data
    new_serializer_data = sorted(
        new_serializer_data, key=lambda i: datetime(int(i['payment_year']), int(i['payment_month']), 1))
    # new_serializer_data = get_modified_payment_details(self.request.query_params.get(
    #     'user'), new_serializer_data, from_month, from_year, to_month, to_year)

    if user_data:
      return Response({
        'status': True,
        'data': new_serializer_data,
        'details': 'Resident payment details is fetched.'
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'status': False,
        'details': 'Resident payment details is not found'
      }, status=status.HTTP_200_OK)


class GetUserPaymentStatusViewset(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsUser]
  
  def list(self, request):
    user = User.objects.get(mobile_number=self.request.user)
    from_month, from_year = self.request.query_params.get(
        'from_month'), self.request.query_params.get('from_year')
    to_month, to_year = self.request.query_params.get(
        'to_month'), self.request.query_params.get('to_year')
    from_month, to_month, from_year, to_year = adjust_date_and_months(
        from_month, to_month, from_year, to_year)

    user_data = users_paid_payment_data(
        user.id, from_month, from_year, to_month, to_year)
    serializer = self.serializer_class(user_data, many=True)

    new_serializer_data = serializer.data
    # new_serializer_data = get_modified_payment_details(user.id, new_serializer_data, from_month, from_year, to_month, to_year)

    due_months = Payment.objects.filter(user=self.request.user, status=Payment.Status.UNPAID)
    due_months = self.serializer_class(due_months, many=True)
    # due_months = get_user_due_months(
    #     self.request.user, from_month, from_year, to_month, to_year)

    if user_data:
      return Response({
        'status': True,
        'data': new_serializer_data,
        'due_months': due_months.data,
        'details': 'User payment details is fetched.'
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'status': False,
        'data': new_serializer_data,
        'due_months': due_months.data,
        'details': 'User payment details is not found'
      }, status=status.HTTP_200_OK)


class GetUserPaymentDetailsViewset(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsUser]

  def list(self, request):
    payment = Payment.objects.filter(user=self.request.user)
    serializer = self.serializer_class(payment, many=True)

    due_months = get_user_due_months(self.request.user)
    
    if payment:
      return Response({
        'status': True,
        'data': serializer.data[-5:],
        'due_months': due_months,
        'details': 'User payments are fetched successfully.'
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'status': False,
        'details': 'User payments are not available.'
      }, status=status.HTTP_200_OK)


# class DeletePaymentDetailsViewset(viewsets.ModelViewSet):
#   queryset = Payment.objects.all()
#   serializer_class = PaymentSerializer
#   permission_classes = [IsAdminUser]

#   def list(self, request):
#     payment_id = self.request.query_params.get('payment_id')
#     payment = Payment.objects.get(id=int(payment_id))

#     if payment:
#       payment.delete()
#       return Response({
#         'status': True,
#         'details': 'Payment details deleted'
#       }, status=status.HTTP_204_NO_CONTENT)
#     else:
#       return Response({
#         'status': False,
#         'details': 'Payment details not found'
#       }, status=status.HTTP_404_NOT_FOUND)


class PendingPaymentViewset(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsAdminUser]
  # pagination_class = StandardResultsSetPagination

  def list(self, request):
    from_month, to_month, from_year, to_year = adjust_date_and_months()
    active_users = User.objects.exclude(role=User.Role.SUPER).exclude(
        role=User.Role.ADMIN).filter(is_active=True)
    user_data = []
    limited_user_data = []
    for user in active_users:
      user_data = user_data + \
          list(Payment.objects.filter(user=user, status=Payment.Status.UNPAID))
      limited_user_data = limited_user_data + \
          list(Payment.objects.filter(user=user, status=Payment.Status.UNPAID))[-3:]
    serializer = self.serializer_class(user_data, many=True)
    limited_serializer = self.serializer_class(limited_user_data, many=True)

    return Response({
        'status': True,
        # 'data': self.paginate_queryset(user_data),
        # 'data': self.get_paginated_response(user_data),
        'data': serializer.data,
        'limited_data': limited_serializer.data,
        'details': 'Users pending payment details is fetched.'
    }, status=status.HTTP_200_OK)
