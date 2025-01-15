from django.contrib import admin
from chemiboostapp.models import UserDetails, Purchase, Party, PurchaseItem
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