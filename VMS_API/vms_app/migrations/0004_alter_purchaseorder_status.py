# Generated by Django 4.2.7 on 2023-11-29 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0003_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('canceled', 'canceled')], default='pending', max_length=100),
        ),
    ]
