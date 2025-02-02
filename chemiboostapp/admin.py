from django.contrib import admin
from chemiboostapp.models import UserDetails, Purchase, Party, PurchaseItem, MedicineStock, Customer, Billing, BillingItem
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class UserDetailsV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID','fullname','companyName','last_update_date')

admin.site.register(UserDetails,UserDetailsV)

class PurchaseV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('purchase_invoice_number','ref_user','Supplier_name')

admin.site.register(Purchase,PurchaseV)


class PartyV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('party_id','ref_user','name','contact_number', 'email')

admin.site.register(Party,PartyV)


class PurchaseItemV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('purchase','company','item_name','batch', 'created_at')

admin.site.register(PurchaseItem,PurchaseItemV)

class MedicineStockV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('company','item_name', 'qty', 'batch', 'created_at')

admin.site.register(MedicineStock,MedicineStockV)



# Customer Admin
class CustomerV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('customer_id', 'ref_user', 'name', 'phone_number', 'created_at')

admin.site.register(Customer, CustomerV)

# Billing Admin
class BillingV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'ref_user', 'total_amount', 'total_GST', 'total_with_GST', 'billing_date', 'billing_time')

admin.site.register(Billing, BillingV)

# BillingItem Admin
class BillingItemV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('billingItemID', 'ref_user', 'item_name', 'batch', 'qty', 'price', 'discount', 'total_with_GST', 'created_at')

admin.site.register(BillingItem, BillingItemV)