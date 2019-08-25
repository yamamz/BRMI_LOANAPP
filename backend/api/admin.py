from django.contrib import admin
from .models import Member,ClusterName,Loan,LoanSchedulePayments,LoanPayment,File

admin.site.register(Member)
admin.site.register(ClusterName)
admin.site.register(Loan)
admin.site.register(LoanSchedulePayments)
admin.site.register(LoanPayment)
admin.site.register(File)



# Register your models here.

