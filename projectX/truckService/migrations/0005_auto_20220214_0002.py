# Generated by Django 3.2.11 on 2022-02-13 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0004_alter_staffexpense_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffexpense',
            name='eidFee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffexpense',
            name='medicalIns',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffexpense',
            name='others',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffexpense',
            name='overTime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffexpense',
            name='totalAmount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffexpense',
            name='visaFee',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]