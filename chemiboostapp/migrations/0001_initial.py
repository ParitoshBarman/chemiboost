# Generated by Django 5.1.4 on 2025-01-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('slID', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=122)),
                ('companyName', models.CharField(max_length=122)),
                ('companyLogo', models.ImageField(upload_to='companyLogoes')),
                ('companylatitude', models.FloatField()),
                ('companylongitude', models.FloatField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('whatsapp', models.CharField(max_length=20)),
                ('wp_access_token', models.TextField(verbose_name='WhatsApp Access Token')),
                ('wp_phonenumber_id', models.CharField(max_length=50, verbose_name='WhatsApp Phone Number ID')),
                ('whatsapp_business_account_id', models.CharField(max_length=50, verbose_name='WhatsApp Business Account ID')),
                ('wp_message_transfer_number', models.CharField(help_text='In E.164 format, e.g., +1234567890', max_length=15, verbose_name='Recipient Phone Number')),
                ('your_webhook_token', models.CharField(max_length=50, verbose_name='Your Webhook Token')),
                ('subscription', models.BooleanField(default=False)),
                ('next_subscription_expiry', models.DateField(verbose_name='Next Subscription Expiry Date')),
                ('totalSpent', models.IntegerField(default=0)),
                ('totalPaymentReceived', models.IntegerField(blank=True, default=0, null=True)),
                ('last_update_date', models.DateField(auto_now=True)),
                ('last_update_time', models.TimeField(auto_now=True)),
            ],
        ),
    ]
