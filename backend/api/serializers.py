from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import Member, Loan, LoanSchedulePayments,ClusterName, LoanPayment

class MemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = Member
		fields = '__all__'

class ClusterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClusterName
		fields = '__all__'



class LoanPaymentSerializer(serializers.ModelSerializer):
	date_of_payment=serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y', 'iso-8601'])
	class Meta:
		model = LoanPayment
		fields = '__all__'



class LoanSchedSerializer(serializers.ModelSerializer):
	date=serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y', 'iso-8601'])
	class Meta:
		model = LoanSchedulePayments
		fields = '__all__'

class LoansSerializer(serializers.ModelSerializer):
	member = MemberSerializer()
	clustername = ClusterSerializer()
	loanscheds=LoanSchedSerializer(many=True)
	loanpayments=LoanPaymentSerializer(many=True)
	class Meta:
		model = Loan
		fields=['id','member','loan_type','loan_mode','clustername','principal','payment_period','loan_period','loan_witness','interest_rate','interest','processing_fee','cbu','loanscheds','loanpayments','date_release','loan_cycle']

class LoanPaymentListSerializer(serializers.ModelSerializer):
	loan = LoansSerializer()
	class Meta:
		model = LoanPayment
		fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
	loanscheds=LoanSchedSerializer(many=True)
	date_release = serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y', 'iso-8601'])
	# member=MemberSerializer()
	class Meta:
		model = Loan
		fields=['id','member','loan_type','loan_mode','clustername','principal','payment_period','loan_period','loan_witness','interest_rate','interest','processing_fee','cbu','loanscheds','date_release','loan_cycle']

	

	def create(self, validated_data):
		loanscheds = validated_data.pop('loanscheds')
		loan = Loan.objects.create(**validated_data)
		for loan_data in loanscheds:
			LoanSchedulePayments.objects.create(loan=loan, **loan_data)
		return loan

	def update(self, instance, validated_data):
		print(instance)

		instance.member = validated_data.get('member', instance.member)
		instance.loan_type = validated_data.get('loan_type', instance.loan_type)
		instance.clustername = validated_data.get('clustername', instance.clustername)
		instance.principal = validated_data.get('principal', instance.principal)
		instance.interest = validated_data.get('interest', instance.interest)
		instance.interest_rate = validated_data.get('interest_rate', instance.interest_rate)
		instance.processing_fee = validated_data.get('processing_fee', instance.processing_fee)
		instance.loan_witness = validated_data.get('loan_witness', instance.loan_witness)
		instance.cbu = validated_data.get('cbu', instance.cbu)
		instance.date_release = validated_data.get('date_release', instance.date_release)
		instance.loan_mode = validated_data.get('loan_mode', instance.loan_mode)
		instance.payment_period = validated_data.get('payment_period', instance.payment_period)
		
		
		instance.save()

		loanscheds = validated_data.get('loanscheds')
		LoanSchedulePayments.objects.filter(loan=instance).delete()

		for item in loanscheds:
			print(item)
			item_id = item.get('id',None)
			print(item_id)
			if item_id:
				inv_item = LoanSchedulePayments.objects.get(pk=item_id)
				inv_item.date = item.get('date', inv_item.date)
				inv_item.principal = item.get('principal', inv_item.principal)
				inv_item.interest = item.get('interest', inv_item.interest)		
				inv_item.save()
			else:
				LoanSchedulePayments.objects.create(loan=instance, **item)

		return instance

