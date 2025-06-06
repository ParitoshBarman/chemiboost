# Generated by Django 5.1.4 on 2025-01-22 15:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemiboostapp', '0012_alter_purchase_party_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='total_amount_with_GST',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='cgst',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Cgst In persentage'),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='sgst',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Sgst In persentage'),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='totalWithGST',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total with GST'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='next_subscription_expiry',
            field=models.DateField(default=datetime.datetime(2025, 2, 21, 21, 9, 30, 771891), verbose_name='Next Subscription Expiry Date'),
        ),
    ]
