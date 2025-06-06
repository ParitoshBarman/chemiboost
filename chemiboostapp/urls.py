from django.contrib import admin
from django.urls import path
from chemiboostapp import views

urlpatterns = urlpatterns = [
    path("", views.index, name='home'),
    path("get_dashboard_data", views.get_dashboard_data, name='get_dashboard_data'),
    path("purchase", views.purchase, name='purchase'),
    path("sales", views.sales, name='sales'),
    path("stock", views.stock, name='stock'),
    path("expiredmedicine", views.expiredmedicine, name='expiredmedicine'),
    path("mycustomers", views.mycustomers, name='mycustomers'),
    path("get-mycustomers/", views.get_mycustomers, name='get_mycustomers'),
    path("pendingpayments", views.pendingpayments, name='pendingpayments'),
    path("mybills", views.mybills, name='mybills'),
    path("testreports", views.testreports, name='testreports'),
    path("announcement", views.announcement, name='announcement'),
    path("accountsettings", views.accountsettings, name='accountsettings'),
    path("login", views.login_control, name='login'),
    path("createaccount", views.createaccount, name='createaccount'),
    path("forgotpassword", views.forgotpassword, name='forgotpassword'),
    path("otp-verification/", views.otp_verification, name="otp_verification"),
    path("get_purchases/", views.get_purchases, name="get_purchases"),
    path('edit-purchase/<int:purchase_id>/', views.edit_purchase, name="edit_purchase"),
    path("get_purchase_items/<int:purchase_id>", views.get_purchase_items, name="get_purchase_items"),
    path("purchase-history", views.purchase_list, name="purchase_list"),
    path("create-bill", views.create_bill, name="create_bill"),
    path("get_billing_data", views.get_billing_data, name="get_billing_data"),
    path("edit-bill/<int:bill_id>", views.edit_bill, name="edit_bill"),
    path("get-bill-details/<str:invoice_id>/", views.get_bill_details, name="get_bill_details"),
    path("create_purchase", views.create_purchase, name="create_purchase"),
    path("delete-purchase/<int:purchase_id>/", views.delete_purchase, name="delete_purchase"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path('addparty', views.add_party, name='add_party'),
    path('editparty/<int:party_id>', views.edit_party, name='edit_party'),
    path('deleteparty/<int:party_id>', views.delete_party, name='delete_party'),
    path("test", views.test, name='test'),
    path("download-invoice-pdf/<int:purchase_id>", views.download_invoice_pdf, name='download_invoice_pdf'),
    path("download-bill-pdf/<int:invoice_id>", views.download_sales_invoice_pdf, name='download_sales_invoice_pdf'),
    path("generate_invoice_pdf/<int:purchase_id>", views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path("get_medicine_stock", views.get_medicine_stock, name='get_medicine_stock'),
    path("get_customers", views.get_customers, name='get_customers'),
    path("get_expired_medicines", views.get_expired_medicines, name='get_expired_medicines'),
]
