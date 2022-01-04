from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from security.serializers import SecuritySerializer, UpdateStatusSerializer, SetTimetableSerializer, GetTimetableSerializer, UpdateSecuritySerializer, DeleteTimeSerializer
from security.models import Security, Timetable
from service_auth.permissions import IsUser, IsUserReadOnly, IsAdminUser
from django.core import serializers as djanog_serializers


class SecurityCreateViewset(viewsets.ViewSet):
  queryset = Security.objects.all()
  serializer_class = SecuritySerializer
  permission_classes = [IsAdminUser]
  parser_classes = (MultiPartParser, FormParser,)

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    if self.request.method == 'GET':
      self.permission_classes = [IsAdminUser | IsUser]
    
    return super().get_permissions()
  
  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      security = Security.objects.create(**serializer.validated_data)
      return Response({
        'status': True,
        'detail': 'Security details added.',
        'data': serializer.data
      }, status=status.HTTP_201_CREATED)
    else:
      return Response({
        'status': False,
        'detail': 'Some fields are missing',
        'data' : serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)


class SecurityUpdateViewset(viewsets.ViewSet):
  queryset = Security.objects.all()
  serializer_class = UpdateSecuritySerializer
  permission_classes = [IsAdminUser]
  # parser_classes = (MultiPartParser, FormParser,)

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    
    return super().get_permissions()
  
  def create(self, request):
    security = Security.objects.get(
        id=int(self.request.data.get('security_id')))
    # serializer = self.serializer_class(data=request.data)
    if security:
      security.full_name = self.request.data.get('full_name')
      security.father_name = self.request.data.get('father_name')
      security.gender = self.request.data.get('gender')
      security.date_of_joining = self.request.data.get('date_of_joining')
      security.permanent_address = self.request.data.get('permanent_address')
      security.date_of_birth = self.request.data.get('date_of_birth')
      security.mobile_number = self.request.data.get('mobile_number')
      security.reference = self.request.data.get('reference')
      security.save()
      return Response("Security person details updated.", status=status.HTTP_200_OK)
    else:
      return Response("Security person not found", status=status.HTTP_404_NOT_FOUND)


class GetAllSecurities(viewsets.ModelViewSet):
  queryset = Security.objects.all()
  serializer_class = SecuritySerializer
  permission_classes = [IsAdminUser]

  def get_queryset(self):
    return Security.objects.all()


class GetActiveSecurities(viewsets.ModelViewSet):
  queryset = Security.objects.all()
  serializer_class = SecuritySerializer
  permission_classes = [IsAdminUser]

  def get_queryset(self):
    return Security.objects.filter(status=Security.Status.ACTIVE)


class GetSecurity(viewsets.ModelViewSet):
  queryset = Security.objects.all()
  serializer_class = SecuritySerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    security = Security.objects.get(
        id=int(self.request.data.get('id')))
    if security:
      return Response({
        'security_id': security.id,
        'full_name': security.full_name,
        'father_name': security.father_name,
        'gender': security.gender,
        'date_of_joining': security.date_of_joining,
        'date_of_birth': security.date_of_birth,
        'permanent_address': security.permanent_address,
        'mobile_number': security.mobile_number,
        'reference': security.reference
      }, status=status.HTTP_200_OK)
    else:
      return Response("Security person not found", status=status.HTTP_404_NOT_FOUND)


class UpdateStatus(viewsets.ViewSet):
  queryset = Security.objects.all()
  serializer_class = UpdateStatusSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      security = Security.objects.get(id=serializer.validated_data.get('security_id'))
      security.status = Security.Status.DEACTIVE if serializer.validated_data.get('status') == Security.Status.ACTIVE else Security.Status.ACTIVE
      security.save()
      return Response({
        'status': True,
        'detail': 'Status updated'
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'status': False,
        'detail': 'Some fields are missing'
      }, status=status.HTTP_400_BAD_REQUEST)


class SetTimeViewset(viewsets.ModelViewSet):
  queryset = Timetable.objects.all()
  serializer_class = SetTimetableSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()

  def create(self, request):
    serializer = self.serializer_class(
        data=request.data, many=isinstance(request.data, list))
    if serializer.is_valid():
      self.perform_create(serializer)
      return Response({
          'status': True,
          'detail': 'Timings added.',
          'data': serializer.data
      }, status=status.HTTP_201_CREATED)
    else:
      return Response({
          'status': False,
          'detail': 'Some fields are missing',
          'data': serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)


class UpdateTimeViewset(viewsets.ModelViewSet):
  queryset = Timetable.objects.all()
  serializer_class = SetTimetableSerializer
  permission_classes = [IsAdminUser]

  def get_permissions(self):
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()

  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      security_time = Timetable.objects.get(id=int(self.request.data.get('id')))
      if security_time and security_time.task_date:
        security_time.security = serializer.validated_data["security"]
        security_time.start_time = serializer.validated_data["start_time"]
        security_time.end_time = serializer.validated_data["end_time"]
        security_time.save()
        return Response({
            'status': True,
            'detail': 'Timings updated.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
      else:
        self.perform_create(serializer)
        return Response({
            'status': True,
            'detail': 'Timings added.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
      return Response({
          'status': False,
          'detail': 'Some fields are missing',
          'data': serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)


class DeleteTimeViewset(viewsets.ViewSet):
  queryset = Timetable.objects.all()
  serializer_class = DeleteTimeSerializer
  permission_classes = [IsAdminUser]

  def create(self, request):
    time = Timetable.objects.get(id=int(self.request.data.get('id')))
    if time:
      time.delete()
      return Response("Time deleted.", status=status.HTTP_200_OK)
    else:
      return Response("Time not found", status=status.HTTP_404_NOT_FOUND)


class GetTimeViewset(viewsets.ModelViewSet):
  queryset = Timetable.objects.all()
  serializer_class = GetTimetableSerializer
  permission_classes = [IsAdminUser | IsUser]

  def get_queryset(self):
    return Timetable.objects.filter(security__status=Security.Status.ACTIVE)

class GetSecurityTimeViewset(viewsets.ModelViewSet):
  queryset = Timetable.objects.all()
  serializer_class = GetTimetableSerializer
  permission_classes = [IsAdminUser | IsUser]

  def get_queryset(self):
    return Timetable.objects.filter(security__status=Security.Status.ACTIVE, security__id=self.request.query_params.get('security_id'))
