# Generated by Django 3.2.13 on 2022-04-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0038_auto_20220425_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='estate_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='contact',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='managing_by',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Real_Estate', 'Real Estate'), ('Other', 'Other')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='staffexpense',
            name='salary_paid_by',
            field=models.CharField(choices=[('exchange', 'Exchange'), ('By Hand', 'By Hand'), ('Both', 'Both')], max_length=100, null=True),
        ),
    ]
