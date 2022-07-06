# Generated by Django 3.2.11 on 2022-04-12 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0027_auto_20220412_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='officeexpense',
            name='vat',
            field=models.IntegerField(default=0, null=True, verbose_name='VAT%'),
        ),
        migrations.AddField(
            model_name='otherexpense',
            name='vat',
            field=models.IntegerField(default=0, null=True, verbose_name='VAT%'),
        ),
        migrations.AddField(
            model_name='truckexpense',
            name='vat',
            field=models.IntegerField(default=0, null=True, verbose_name='VAT%'),
        ),
    ]