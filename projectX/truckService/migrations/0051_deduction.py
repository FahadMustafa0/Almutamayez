# Generated by Django 3.2.13 on 2022-05-06 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0050_staffexpense_deduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='deduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
                ('amount', models.IntegerField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ss', to='truckService.staffprofile')),
            ],
        ),
    ]