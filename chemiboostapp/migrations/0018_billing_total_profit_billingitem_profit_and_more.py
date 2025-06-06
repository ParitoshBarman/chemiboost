# Generated by Django 5.1.4 on 2025-02-15 18:35

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemiboostapp', '0017_billing_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='total_profit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total Profit'),
        ),
        migrations.AddField(
            model_name='billingitem',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Profit'),
        ),
        migrations.AlterField(
            model_name='billing',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing', to='chemiboostapp.customer'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='next_subscription_expiry',
            field=models.DateField(default=datetime.datetime(2025, 3, 18, 0, 5, 30, 252335), verbose_name='Next Subscription Expiry Date'),
        ),
    ]
