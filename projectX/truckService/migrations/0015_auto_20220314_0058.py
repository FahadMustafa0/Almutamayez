# Generated by Django 3.2.11 on 2022-03-13 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0014_allpayments_tripsamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='truckexpense',
            name='fuel_kilometers',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='truckexpense',
            name='fuel_litters',
            field=models.IntegerField(default=0, null=True),
        ),
    ]