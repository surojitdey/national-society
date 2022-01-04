from django.urls import path, include
from rest_framework import routers

from security.views import *

router = routers.DefaultRouter()

router.register('create-security', SecurityCreateViewset)
router.register('update-security', SecurityUpdateViewset)
router.register('get-security-by-id', GetSecurity)
router.register('get-security', GetAllSecurities)
router.register('get-active-security', GetActiveSecurities)
router.register('update-security-status', UpdateStatus)
router.register('set-security-time', SetTimeViewset)
router.register('get-security-time', GetTimeViewset)
router.register('delete-security-time', DeleteTimeViewset)
router.register('update-security-time', UpdateTimeViewset)
router.register('get-individual-security-time', GetSecurityTimeViewset)

urlpatterns = [
    path('', include(router.urls))
]
