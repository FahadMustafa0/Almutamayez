# Generated by Django 3.2.11 on 2022-03-10 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('truckService', '0012_attendance_leaves'),
    ]

    operations = [
        migrations.AddField(
            model_name='allpayments',
            name='tax',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='truckService.staffprofile'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='month',
            field=models.CharField(choices=[('Jan', 'Jan'), ('Feb', 'Feb'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('Jun', 'Jun'), ('July', 'July'), ('August', 'August'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec')], max_length=250),
        ),
    ]