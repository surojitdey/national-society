from django.urls import path, include
from rest_framework import routers

from society.views import *

router = routers.DefaultRouter()

router.register('create-society', SocietyCreateView)
router.register('check-registration-validity', CheckRagistrationValidityViewset)

urlpatterns = [
    path('', include(router.urls))
]
