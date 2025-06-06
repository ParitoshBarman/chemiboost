# Generated by Django 5.1.4 on 2025-01-22 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemiboostapp', '0013_purchase_total_amount_with_gst_purchaseitem_cgst_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='totalGSTamount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total GST amount'),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='totalGSTamount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total GST amount'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='next_subscription_expiry',
            field=models.DateField(default=datetime.datetime(2025, 2, 21, 21, 21, 41, 867632), verbose_name='Next Subscription Expiry Date'),
        ),
    ]
