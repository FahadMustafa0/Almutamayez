# Generated by Django 3.2.13 on 2022-05-22 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0060_tripdata_total_discharge_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripdata',
            name='DriverName',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DriverName', to='truckService.staffprofile'),
        ),
    ]
