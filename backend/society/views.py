from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from society.models import Society
from society.serializers import SocietySerializer, RegistrationValiditySerializer
from users.models import User


class SocietyCreateView(viewsets.ViewSet):
  queryset = Society.objects.all()
  serializer_class = SocietySerializer
  permission_classes = [AllowAny]

  def create(self, request):
    serializer = self.serializer_class(data=request.data)

    if(serializer.is_valid()):
      society = None
      try:
        society = serializer.save()
        user_data = dict()
        user_data['society'] = society
        user_data['password'] = 'AdminPassword'
        user_data['full_name'] = request.data['society_name']
        user_data['email'] = request.data['email']
        user_data['mobile_number'] = request.data['mobile_number']
        user_data['address'] = request.data['address']
        user = User.objects.create_admin(**user_data)
      except:
        if society:
          society.delete()
        return Response({
          'status': False,
          'details': 'Society creation failed.'
        }, status=status.HTTP_400_BAD_REQUEST)
      return Response({
        'status': True,
        'details': 'Society registration successful.'
      }, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckRagistrationValidityViewset(viewsets.ViewSet):
  queryset = Society.objects.all()
  serializer_class = RegistrationValiditySerializer
  permission_classes = [AllowAny]

  def create(self, request):
    if('society_registration_number' in self.request.data):
      society = Society.objects.filter(
          registration_number=self.request.data['society_registration_number'])
      if len(society):
        return Response({
            "status": True,
            "isValid": True,
            "detail": "Society exist."
        }, status=status.HTTP_200_OK)
      else:
        return Response({
            "status": True,
            "isValid": False,
            "detail": "Registration is not valid."
        }, status=status.HTTP_200_OK)
    else:
      return Response({
          'status': False,
          'detail': 'Registration ID is not provided.'
      }, status=status.HTTP_400_BAD_REQUEST)

