# Generated by Django 2.1.1 on 2019-08-18 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20190818_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanschedulepayments',
            name='loan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loanscheds', to='api.Loan'),
        ),
    ]
