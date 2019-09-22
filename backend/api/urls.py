"""
API url patterns
"""
from django.urls import path, re_path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
router = routers.DefaultRouter()
router.register('members', views.MemberViewSet)
router.register('loans', views.LoanViewSet)
router.register('loanss', views.LoansViewSet)
router.register('loanpaymentscheds', views.LoanSchedViewset)
router.register('loanpayment', views.LoanPaymentViewSet)
router.register('clusters', views.ClusterViewSet)


urlpatterns = [
    path("hello", views.hello_world),
    path('v1/', include(router.urls)),
    path('v1/loanpaymentlist/<loan_id>',views.LoanPaymentList.as_view(),name="loanpayments"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/deletescheds/<int:id>',views.deleteSchedules,name='delete-scheds'),
    path('v1/deletepayments/<int:id>',views.deletePayments,name='delete-payments'),
    
    path('v1/searchPayments/<int:id>',views.searchPaymentsAndSchedules,name='search-scheds'),
    

]