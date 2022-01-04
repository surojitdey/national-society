from django.urls import path, include
from rest_framework import routers

from fees.views import *

router = routers.DefaultRouter()

router.register('fees', FeesItemViewset)
router.register('update-fees', UpdateFeesItemViewset)
router.register('payment-fees', PaymentViewset)
router.register('payment-status', GetPaymentStatusViewset)
router.register('user-payment-status', GetUserPaymentStatusViewset)
router.register('user-payment', GetUserPaymentDetailsViewset)
# router.register('delete-user-payment', DeletePaymentDetailsViewset)
router.register('pending-user-payment', PendingPaymentViewset)

urlpatterns = [
    path('', include(router.urls))
]
