# Generated by Django 2.1.1 on 2019-08-15 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190813_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='date_release',
            field=models.DateField(blank=True, null=True),
        ),
    ]
