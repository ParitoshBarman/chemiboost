# Generated by Django 5.1.4 on 2025-01-14 14:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemiboostapp', '0005_purchase_party'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='chemiboostapp.party'),
        ),
    ]
