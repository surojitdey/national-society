import json
from json import JSONEncoder

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView


from config_ui.models import *
from config_ui.serializers import *
from service_auth.permissions import IsUser, IsUserReadOnly, IsAdminUser


class SettingViewset(viewsets.ModelViewSet):
  queryset = SettingDetails.objects.all()
  serializer_class = SettingSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = (IsAdminUser,)
    elif self.request.method == 'PUT':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'GET':
      self.permission_classes = [AllowAny]

    return super(SettingViewset, self).get_permissions()
  
  def get_queryset(self):
    return SettingDetails.objects.filter(society=self.request.user.society)

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status.HTTP_201_CREATED)


class UpdateSettingViewset(viewsets.ViewSet):
  queryset = SettingDetails.objects.all()
  serializer_class = SettingSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = (IsAdminUser,)
    elif self.request.method == 'PUT':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'PATCH':
      self.permission_classes = [IsAdminUser]
    elif self.request.method == 'GET':
      self.permission_classes = [AllowAny]

    return super(UpdateSettingViewset, self).get_permissions()

  def create(self, request, *args, **kwargs):
    setting_details = SettingDetails.objects.get(id=int(self.request.data.get('id')))
    if setting_details:
      setting_details.community_name = self.request.data.get('community_name')
      setting_details.appartment_name = self.request.data.get('appartment_name')
      setting_details.address_one = self.request.data.get('address_one')
      setting_details.address_two = self.request.data.get('address_two')
      setting_details.city = self.request.data.get('city')
      setting_details.pincode = self.request.data.get('pincode')
      setting_details.contact_number = self.request.data.get('contact_number')
      setting_details.email = self.request.data.get('email')
      setting_details.show_address = self.request.data.get('show_address')
      setting_details.show_number = self.request.data.get('show_number')
      setting_details.show_email = self.request.data.get('show_email')
      setting_details.enable_events = self.request.data.get('enable_events')
      setting_details.enable_news = self.request.data.get('enable_news')
      setting_details.enable_posts = self.request.data.get('enable_posts')
      setting_details.show_complaints = self.request.data.get(
          'show_complaints')
      setting_details.save()
      return Response('setting details updated', status.HTTP_201_CREATED)
    else:
      return Response("setting details not found", status=status.HTTP_404_NOT_FOUND)
