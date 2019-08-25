from django.db import models

# Create your models here.

class Member(models.Model):
    account_number=models.CharField(max_length=100,null=True, blank=True,unique=True)
    fname=models.CharField(max_length=100)
    mname=models.CharField(max_length=100,null=True,blank=True)
    lname=models.CharField(max_length=100)
    age=models.IntegerField(default=0,null=True,blank=True)
    gender=models.CharField(max_length=30)
    occupation=models.CharField(max_length=300,null=True,blank=True)
    civil_status=models.CharField(max_length=50)
    partner_name=models.CharField(max_length=200,null=True,blank=True)
    address=models.CharField(max_length=200)
    mobile_number=models.CharField(max_length=14)
    monthly_income=models.BigIntegerField(default=0)


    def __str__(self):
        return self.fname +' '+self.lname

class ClusterName(models.Model):
    name=models.CharField(max_length=200)

class Loan(models.Model):
    loan_cycle= models.IntegerField(default=1)
    loan_type=models.IntegerField(default=1)
    loan_mode=models.IntegerField(default=1)

    member=models.ForeignKey(Member,on_delete=models.PROTECT,related_name="loanapplications")
    clustername=models.ForeignKey(ClusterName,on_delete=models.PROTECT,related_name="loanapplications")
    principal=models.DecimalField(max_digits=40,decimal_places=2)
    interest_rate=models.DecimalField(max_digits=40,decimal_places=2)
    interest=models.DecimalField(max_digits=40,decimal_places=2)
    processing_fee=models.DecimalField(max_digits=40,decimal_places=2,null=True,blank=True)
    loan_period=models.FloatField(default=0.0)
    payment_period=models.IntegerField(default=1)
    loan_witness=models.CharField(max_length=200,null=True,blank=True)
    cbu=models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    date_release=models.DateField(null=True, blank=True)

class LoanPayment(models.Model):
    loan=models.ForeignKey(Loan,on_delete=models.PROTECT,related_name="loanpayments")
    date_of_payment = models.DateField()
    beginning_balance = models.DecimalField(max_digits=40,decimal_places=2)
    paid_interest = models.DecimalField(max_digits=40,decimal_places=2)
    paid_principal = models.DecimalField(max_digits=40,decimal_places=2)
    ending_balance = models.DecimalField(max_digits=40,decimal_places=2)

class File(models.Model):
    file = models.FileField(upload_to='file/')

class LoanSchedulePayments(models.Model):
    loan=models.ForeignKey(Loan,on_delete=models.CASCADE,null=True,related_name="loanscheds")
    date=models.DateField()
    principal=models.DecimalField(max_digits=40,decimal_places=2)
    interest=models.DecimalField(max_digits=40,decimal_places=2)



    

    
