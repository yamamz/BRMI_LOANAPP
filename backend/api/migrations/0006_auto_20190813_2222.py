# Generated by Django 2.1.1 on 2019-08-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_loan_loan_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='payment_period',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_witness',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
