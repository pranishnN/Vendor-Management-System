# Generated by Django 4.2.7 on 2023-11-29 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0002_alter_purchaseorder_acknowledgment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('new order', 'new order'), ('completed', 'completed')], default='new order', max_length=100),
        ),
    ]
