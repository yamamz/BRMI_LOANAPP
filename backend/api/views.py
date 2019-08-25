from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from .serializers import LoanPaymentListSerializer, MemberSerializer,LoansSerializer, LoanSchedSerializer,LoanSerializer,ClusterSerializer, LoanPaymentSerializer
from .models import Member,Loan,LoanSchedulePayments,ClusterName, LoanPayment

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def hello_world(request):
    return Response({'Hello world'})

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    permission_classes=((IsAuthenticated,))
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class LoanPaymentList(generics.ListAPIView):
	serializer_class = LoanPaymentListSerializer
	permission_classes = (IsAuthenticated,)


	def get_queryset(self):
		loan_pk=self.kwargs['loan_id']
		loan=get_object_or_404(Loan,pk=loan_pk)

		return LoanPayment.objects.filter(loan=loan)


class LoanPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    permission_classes=((IsAuthenticated,))
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer

class LoansViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    permission_classes=((IsAuthenticated,))
    queryset = Loan.objects.select_related("member").all()
    serializer_class = LoansSerializer

class LoanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    permission_classes=((IsAuthenticated,))
    queryset = Loan.objects.select_related("member").all()
    serializer_class = LoanSerializer

class ClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    permission_classes=((IsAuthenticated,))
    queryset = ClusterName.objects.all()
    serializer_class = ClusterSerializer

class LoanSchedViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    permission_classes=((IsAuthenticated,))
    queryset = LoanSchedulePayments.objects.all()
    serializer_class = LoanSchedSerializer
