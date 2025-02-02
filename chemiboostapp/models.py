from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder  # Encoder for JSON

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="details")
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    companyName = models.CharField(max_length=122)
    companyLogo = models.ImageField( upload_to="companyLogoes")
    companylatitude = models.FloatField(default=0)
    companylongitude = models.FloatField(default=0)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    whatsapp = models.CharField(max_length=20)

    # wpAccessToken
    wp_access_token = models.TextField(verbose_name="WhatsApp Access Token")
    # wpPhonenumberID
    wp_phonenumber_id = models.CharField(max_length=50, verbose_name="WhatsApp Phone Number ID")
    # WhatsAppBusinessAccountID
    whatsapp_business_account_id = models.CharField(max_length=50, verbose_name="WhatsApp Business Account ID")
    # wpmessageTransferNumber
    wp_message_transfer_number = models.CharField(
        max_length=15, verbose_name="Recipient Phone Number", help_text="In E.164 format, e.g., +1234567890"
    )

    your_webhook_token = models.CharField(max_length=50, verbose_name="Your Webhook Token")
    
    subscription = models.BooleanField(default=False)
    next_subscription_expiry = models.DateField(verbose_name="Next Subscription Expiry Date", default=datetime.now()+timedelta(days=30))
    
    totalSpent = models.IntegerField(default=0)
    totalPaymentReceived = models.IntegerField(null=True,blank=True,default=0)
    last_update_date = models.DateField(auto_now=True)
    last_update_time = models.TimeField(auto_now=True)
    # joiningdate = models.DateField(auto_now_add=True)


class Party(models.Model):
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='parties')
    party_id = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255)
    name = models.CharField(max_length=255, verbose_name="Party Name")
    contact_number = models.CharField(max_length=15, verbose_name="Contact Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email Address")
    gst_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="GST Number")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    totalExpence = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")



class Purchase(models.Model):
    party = models.ForeignKey(Party, on_delete=models.DO_NOTHING, related_name='purchases')
    purchase_invoice_number = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255)
    Supplier_name = models.CharField(max_length=255)
    Supplier_contact_number = models.CharField(max_length=15, blank=True, null=True)
    Supplier_email = models.EmailField(blank=True, null=True)
    Supplier_address = models.TextField(blank=True, null=True)
    Supplier_gst = models.CharField(max_length=20, blank=True, null=True)

    purchase_items = models.JSONField(encoder=DjangoJSONEncoder, default=list)  # JSONField for storing items

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount_with_GST = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    totalGSTamount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total GST amount")

    purchase_date = models.DateField()
    last_update_date = models.DateField(auto_now=True)
    last_update_time = models.TimeField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)



class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    PurchaseItemID = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255, default="")
    company = models.CharField(max_length=255, verbose_name="Company")
    item_name = models.CharField(max_length=255, verbose_name="Item Name")
    batch = models.CharField(max_length=100, verbose_name="Batch")
    exp_date = models.DateField(null=True, blank=True, verbose_name="Expiration Date")
    mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="MRP")
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rate")
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Cgst In persentage")
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Sgst In persentage")
    qty = models.IntegerField(verbose_name="Quantity")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    totalGSTamount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total GST amount")
    totalWithGST = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total with GST")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

class MedicineStock(models.Model):
    PurchaseItemID = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255, default="")
    company = models.CharField(max_length=255, verbose_name="Company")
    item_name = models.CharField(max_length=255, verbose_name="Item Name")
    batch = models.CharField(max_length=100, verbose_name="Batch")
    exp_date = models.DateField(null=True, blank=True, verbose_name="Expiration Date")
    mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="MRP")
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rate")
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Cgst In persentage")
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Sgst In persentage")
    qty = models.IntegerField(verbose_name="Quantity")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    totalGSTamount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total GST amount")
    totalWithGST = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total with GST")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")



class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, verbose_name="Customer Name")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Email Address")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    # gst_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="GST Number")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")


class Billing(models.Model):
    invoice_number = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255, default="")
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='purchases')
    customer_name = models.CharField(max_length=255, verbose_name="Customer Name")
    customer_contact = models.CharField(max_length=15, blank=True, null=True, verbose_name="Customer Contact")
    customer_email = models.EmailField(blank=True, null=True, verbose_name="Customer Email")
    customer_address = models.TextField(blank=True, null=True, verbose_name="Customer Address")

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Amount")
    total_GST = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total GST Amount")
    total_with_GST = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Amount with GST")

    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Paid Amount")
    payment_method = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking')
    ], verbose_name="Payment Method")

    payment_status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
        ('Completed', 'Completed')
    ], default='Pending', verbose_name="Payment Status")

    billing_date = models.DateField(auto_now_add=True, verbose_name="Billing Date")
    billing_time = models.TimeField(auto_now_add=True, verbose_name="Billing Time")
    last_update_date = models.DateField(auto_now=True, verbose_name="Last Update Date")
    last_update_time = models.TimeField(auto_now=True, verbose_name="Last Update Time")


class BillingItem(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name='items')
    billingItemID = models.AutoField(primary_key=True)
    ref_user = models.CharField(max_length=255, default="")
    item_name = models.CharField(max_length=255, verbose_name="Item Name")
    batch = models.CharField(max_length=100, verbose_name="Batch")
    
    qty = models.IntegerField(verbose_name="Quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rate per Unit")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Discount Amount")  # New Discount Field
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="CGST %")
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="SGST %")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    total_GST_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total GST Amount")
    total_with_GST = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total with GST")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

