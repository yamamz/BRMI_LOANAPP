# Generated by Django 2.1.1 on 2019-08-19 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20190818_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_payment', models.DateField()),
                ('beginning_balance', models.DecimalField(decimal_places=2, max_digits=40)),
                ('paid_interest', models.DecimalField(decimal_places=2, max_digits=40)),
                ('paid_principal', models.DecimalField(decimal_places=2, max_digits=40)),
                ('ending_balance', models.DecimalField(decimal_places=2, max_digits=40)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loanpayments', to='api.Loan')),
            ],
        ),
    ]
