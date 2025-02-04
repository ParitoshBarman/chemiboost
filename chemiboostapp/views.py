from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chemiboostapp import whatsappcloud
from django.contrib.auth.decorators import login_required
from chemiboostapp.models import Party, UserDetails, Purchase, PurchaseItem, MedicineStock, Customer, Billing, BillingItem
from django.core import serializers
from datetime import datetime
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa
import threading
from chemiboostapp import extrafunction
from django.db.models import Q

mytoken = "hjhhkjhjhkjhjkghghjgjhghg"

# Helper function to convert DD-MM-YYYY to YYYY-MM-DD for Django filtering
def convert_to_iso_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None  # Ignore if not a valid date format

# Create your views here.
def index(request):
    return render(request, "index.html")
def purchase(request):
    PartyData = Party.objects.filter(user_details=UserDetails.objects.get(user=User.objects.get(username=request.user.username)))
    PartyData = serializers.serialize('json', PartyData)
    return render(request, "purchase.html", {"parties":PartyData})
def sales(request):
    return render(request, "sales.html")
def stock(request):
    # Fetch all stock items from the database
    stock_items = MedicineStock.objects.all()

    # Prepare stock data for rendering in the template
    stock_data = [
        {
            "name": item.item_name,
            "quantity": item.qty
        }
        for item in stock_items
    ]

    # Count total products
    total_products = len(stock_data)

    # Count out-of-stock items
    out_of_stock = sum(1 for item in stock_data if item["quantity"] == 0)

    # Count in-stock items
    in_stock = total_products - out_of_stock

    # Calculate total quantity of all medicines
    total_quantity = sum(item["quantity"] for item in stock_data)

    context = {
        "stock_data": stock_data,
        "total_products": total_products,
        "out_of_stock": out_of_stock,
        "in_stock": in_stock,
        "total_quantity": total_quantity
    }

    # return render(request, "stock.html", context)
    return render(request, "stock.html", context)
def expiredmedicine(request):
    return render(request, "expiredmedicine.html")
def mycustomers(request):
    return render(request, "mycustomers.html")
def pendingpayments(request):
    return render(request, "pendingpayments.html")
def mybills(request):
    return render(request, "mybills.html")
def testreports(request):
    return render(request, "testreports.html")
def announcement(request):
    return render(request, "announcement.html")
def accountsettings(request):
    return render(request, "accountsettings.html")

# Login View
def login_control(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')


# Create Account View
def createaccount(request):
    if request.method == 'POST':
        username = request.POST['phone']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('createaccount')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('createaccount')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('createaccount')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name.split(" ")[0], last_name=name.split(" ")[1])
        user.save()
        user_details = UserDetails(user=user, fullname=name, phone=request.POST['phone'], email=email)
        user_details.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')
    return render(request, "createaccount.html")


# Mock OTP for demonstration
MOCK_OTP = "123456"

def otp_verification(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        if entered_otp == MOCK_OTP:
            messages.success(request, "OTP Verified Successfully!")
            return redirect("success_page")  # Replace 'success_page' with the actual route name
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("otp_verification")
    return render(request, "otp_verification.html")

def resend_otp(request):
    # Logic to resend the OTP
    # Replace with actual SMS/Email API call for production
    return JsonResponse({"message": "OTP has been resent successfully!"})



def forgotpassword(request):
    return render(request, "forgotpassword.html")

@csrf_exempt
def create_bill(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer_name = data.get("customer_name", "")
            customer_contact = data.get("customer_contact", "")
            billing_date = data.get("billing_date")
            total_amount = data.get("total_amount")
            total_GST = data.get("total_GST")
            total_with_GST = data.get("total_with_GST")
            billing_items = data.get("billing_items", [])

             # Ensure required fields are present
            if not customer_contact or not customer_name:
                return JsonResponse({"error": "Customer name and phone number are required"}, status=400)

            if not request.user.is_authenticated:
                return JsonResponse({"error": "User authentication required"}, status=401)
            
            # Process billing items and update stock
            for item in billing_items:
                batch = item["batch"]
                qty_to_sell = item["qty"]
                item_name = item["item_name"]

                # Check if stock exists
                try:
                    stock = MedicineStock.objects.get(ref_user=request.user.username, batch=batch)

                    if stock.qty < qty_to_sell:
                        return JsonResponse({"error": f"Insufficient stock for batch {batch}, Name: {item_name}. Available: {stock.qty}, Required: {qty_to_sell}"}, status=400)


                except MedicineStock.DoesNotExist:
                    return JsonResponse({"error": f"Stock not found for batch {batch}, Name: {item_name}"}, status=404)



            # Check if customer exists based on ref_user and phone_number, else create a new customer
            customer, created = Customer.objects.get_or_create(
                ref_user=request.user.username,  # Assuming ref_user is the logged-in user's username
                phone_number=customer_contact,
                defaults={"name": customer_name}
            )


            # Create a new billing record
            billing = Billing.objects.create(
                customer=customer,
                ref_user=request.user.username,
                customer_name=customer_name,
                customer_contact=customer_contact,
                total_amount=total_amount,
                total_GST=total_GST,
                total_with_GST=total_with_GST
            )

            # Save all billing items
            for item in billing_items:
                BillingItem.objects.create(
                    billing=billing,
                    ref_user=request.user.username,
                    item_name=item["item_name"],
                    batch=item["batch"],
                    qty=item["qty"],
                    price=item["price"],
                    discount=item["discount"],
                    cgst=item["cgst"],
                    sgst=item["sgst"],
                    total=item["total"],
                    total_GST_amount=item["total_GST_amount"],
                    total_with_GST=item["total_with_GST"]
                )

            # Process billing items and update stock
            for item in billing_items:
                batch = item["batch"]
                qty_to_sell = item["qty"]

                # Check if stock exists
                try:
                    stock = MedicineStock.objects.get(ref_user=request.user.username, batch=batch)

                    if stock.qty < qty_to_sell:
                        return JsonResponse({"error": f"Insufficient stock for batch {batch}. Available: {stock.qty}, Required: {qty_to_sell}"}, status=400)

                    # Deduct the sold quantity
                    stock.qty = F("qty") - qty_to_sell
                    stock.save()

                except MedicineStock.DoesNotExist:
                    return JsonResponse({"error": f"Stock not found for batch {batch}"}, status=404)


            return JsonResponse({"message": "Billing record created successfully", "invoice_number": billing.invoice_number}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_billing_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User authentication required"}, status=401)

    query = request.GET.get("query", "").lower()
    status_filter = request.GET.get("status", "all").lower()
    page = int(request.GET.get("page", 1))  # Default to page 1
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page

    # Filter by user
    bills = Billing.objects.filter(ref_user=request.user.username)

    # Apply search filter (customer name, invoice number, or date)
    if query:
        query_date = convert_to_iso_date(query)  # Convert dd-mm-yyyy to YYYY-MM-DD
        bills = bills.filter(
            Q(invoice_number__icontains=query) |  # Search by Invoice Number
            Q(customer_name__icontains=query) |  # Search by Customer Name
            (Q(billing_date=query_date) if query_date else Q())  # Search by Date
        )

    # Apply status filter
    if status_filter != "all":
        bills = bills.filter(payment_status__iexact=status_filter)

    # Paginate results
    paginator = Paginator(bills, per_page)
    paginated_bills = paginator.get_page(page)

    # Format response data
    data = list(paginated_bills.object_list.values(
        "invoice_number", "customer_name", "customer_contact", "billing_date", "total_amount", "payment_status"
    ))

    for bill in data:
        bill["customerName"] = bill.pop("customer_name")
        bill["customer_contact"] = bill.pop("customer_contact")
        bill["billDate"] = bill.pop("billing_date").strftime("%d-%m-%Y")  # Format date as dd-mm-yyyy
        bill["totalAmount"] = bill.pop("total_amount")
        bill["status"] = bill.pop("payment_status").lower()

    return JsonResponse({
        "bills": data,
        "total_pages": paginator.num_pages,
        "current_page": paginated_bills.number,
        "has_next": paginated_bills.has_next(),
        "has_previous": paginated_bills.has_previous(),
    }, safe=False, status=200)

def purchase_list(request):
    return render(request, "PurchaseList.html")

def get_purchases(request):
    """Fetch paginated purchases and their items with optional filtering."""
    # Get the authenticated user
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated"}, status=401)
    try:
        purchases = Purchase.objects.filter(ref_user=user).order_by("-purchase_date")

        # 🔍 Filtering by date range
        start_date = request.GET.get("start_date")  # Format: YYYY-MM-DD
        end_date = request.GET.get("end_date")  # Format: YYYY-MM-DD
        supplier_name = request.GET.get("supplier")  # Optional supplier name filter
        contact_number = request.GET.get("contact")  # Optional contact number filter

        if start_date and end_date:
            purchases = purchases.filter(purchase_date__range=[start_date, end_date])
        
        if supplier_name:
            purchases = purchases.filter(Supplier_name__icontains=supplier_name)
        
        if contact_number:
            purchases = purchases.filter(Supplier_contact_number__icontains=contact_number)

        # 📄 Pagination
        page = request.GET.get("page", 1)  # Default to page 1
        per_page = 10  # Show 10 records per page
        paginator = Paginator(purchases, per_page)
        paginated_purchases = paginator.get_page(page)

        purchases_data = []
        for purchase in paginated_purchases:
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            items_list = [
                {
                    "Company": item.company,
                    "ItemName": item.item_name,
                    "Batch": item.batch,
                    "ExpDate": item.exp_date.strftime("%Y-%m-%d") if item.exp_date else None,
                    "MRP": item.mrp,
                    "Rate": item.rate,
                    "Qty": item.qty,
                    "Total": item.total,
                    "cgst": item.cgst,
                    "sgst": item.sgst,
                    "totalGSTamount": item.totalGSTamount,
                    "totalWithGST": item.totalWithGST,
                }
                for item in purchase_items
            ]

            purchases_data.append({
                "id": purchase.pk,
                "Supplier_name": purchase.Supplier_name,
                "Supplier_contact_number": purchase.Supplier_contact_number,
                "purchase_date": purchase.purchase_date.strftime("%Y-%m-%d"),
                "total_amount": purchase.total_amount,
                "total_amount_with_GST": purchase.total_amount_with_GST,
                "totalGSTamount": purchase.totalGSTamount,
                "purchase_items": items_list
            })

        return JsonResponse({
            "purchases": purchases_data,
            "total_pages": paginator.num_pages,
            "current_page": paginated_purchases.number
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_purchase_items(request, purchase_id):
    """
    Fetches purchase details and items based on purchase_id.
    Returns JSON response for the frontend modal.
    """
    try:
        # Fetch the purchase details
        purchase = get_object_or_404(Purchase, purchase_invoice_number=purchase_id)

        # Fetch all items associated with this purchase
        items = PurchaseItem.objects.filter(purchase=purchase)

        # Structure the response data
        purchase_data = {
            "purchase_invoice_number": purchase.purchase_invoice_number,
            "Supplier_name": purchase.Supplier_name,
            "Supplier_contact_number": purchase.Supplier_contact_number,
            "Supplier_email": purchase.Supplier_email,
            "Supplier_address": purchase.Supplier_address,
            "Supplier_gst": purchase.Supplier_gst,
            "totalGSTamount": purchase.totalGSTamount,
            "total_amount_with_GST": purchase.total_amount_with_GST,
            "total_amount": str(purchase.total_amount),  # Convert Decimal to string for JSON compatibility
            "purchase_date": purchase.purchase_date.strftime("%Y-%m-%d"),
            "items": [
                {
                    "company": item.company,
                    "item_name": item.item_name,
                    "batch": item.batch,
                    "exp_date": item.exp_date.strftime("%Y-%m-%d") if item.exp_date else None,
                    "mrp": str(item.mrp),
                    "rate": str(item.rate),
                    "qty": item.qty,
                    "total": str(item.total),
                    "cgst": item.cgst,
                    "sgst": item.sgst,
                    "totalGSTamount": item.totalGSTamount,
                    "totalWithGST": item.totalWithGST,
                }
                for item in items
            ],
        }

        return JsonResponse({"success": True, "purchase": purchase_data})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt  # Use this only if CSRF protection is disabled for this endpoint
def create_purchase(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from request

            # Get the authenticated user
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "User is not authenticated"}, status=401)

            # Get the user's UserDetails
            try:
                user_details = UserDetails.objects.get(user=user)
            except UserDetails.DoesNotExist:
                return JsonResponse({"error": "User details not found"}, status=404)

            # Get the party details
            try:
                party = Party.objects.get(party_id=data.get("party_id"), user_details=user_details)
            except Party.DoesNotExist:
                return JsonResponse({"error": "Party not found"}, status=404)

            # Create a new Purchase record
            purchase = Purchase.objects.create(
                party=party,
                ref_user=user.username,
                Supplier_name=data.get("Supplier_name"),
                Supplier_contact_number=data.get("party_contact_number"),
                purchase_date=datetime.strptime(data.get("purchase_date"), "%Y-%m-%d").date(),
                total_amount=data.get("total_amount"),
                purchase_items=data.get("purchase_items"),
                total_amount_with_GST=data.get("total_amount_with_GST"),
                totalGSTamount=data.get("totalGSTamount"),
            )

            # Create PurchaseItem records
            purchase_items = data.get("purchase_items", [])
            for item in purchase_items:
                PurchaseItem.objects.create(
                    purchase=purchase,
                    company=item.get("Company"),
                    item_name=item.get("ItemName"),
                    batch=item.get("Batch"),
                    exp_date=datetime.strptime(item.get("ExpDate"), "%Y-%m-%d").date() if item.get("ExpDate") else None,
                    mrp=item.get("MRP"),
                    rate=item.get("Rate"),
                    qty=item.get("Qty"),
                    total=item.get("Total"),
                    cgst=item.get("cgst"),
                    sgst=item.get("sgst"),
                    totalGSTamount=item.get("totalGSTamount"),
                    totalWithGST=item.get("totalWithGST"),
                )

                # Update or create stock
                stock, created = MedicineStock.objects.get_or_create(
                    ref_user=user.username,
                    batch=item["Batch"],
                    defaults={
                        "company": item["Company"],
                        "item_name": item["ItemName"],
                        "exp_date": datetime.strptime(item.get("ExpDate"), "%Y-%m-%d").date() if item.get("ExpDate") else None,
                        "qty": item["Qty"],
                        "mrp": item["MRP"],
                        "rate": item["Rate"],
                        "cgst": item["cgst"],
                        "sgst": item["sgst"],
                        "total": item["Total"],
                        "totalGSTamount": item["totalGSTamount"],
                        "totalWithGST": item["totalWithGST"],
                    }
                )

                if not created:
                    # If stock exists, update quantity and expiration date
                    stock.qty = F("qty") + item["Qty"]
                    stock.exp_date = datetime.strptime(item.get("ExpDate"), "%Y-%m-%d").date() if item.get("ExpDate") else None
                    stock.save()


            return JsonResponse({"message": "Purchase created and stock updated successfully", "purchase_invoice_number":purchase.purchase_invoice_number}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def edit_purchase(request, purchase_id):
    if request.method == "PUT" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)

            # Get the purchase object
            purchase = get_object_or_404(Purchase, purchase_invoice_number=purchase_id)

            # Update purchase details
            purchase.Supplier_name = data.get("Supplier_name", purchase.Supplier_name)
            purchase.Supplier_contact_number = data.get("Supplier_contact_number", purchase.Supplier_contact_number)
            purchase.Supplier_email = data.get("Supplier_email", purchase.Supplier_email)
            purchase.Supplier_address = data.get("Supplier_address", purchase.Supplier_address)
            purchase.Supplier_gst = data.get("Supplier_gst", purchase.Supplier_gst)
            purchase.total_amount = data.get("total_amount", purchase.total_amount)
            purchase.purchase_date = data.get("purchase_date", purchase.purchase_date)
            purchase.totalGSTamount = data.get("totalGSTamount", purchase.totalGSTamount)
            purchase.total_amount_with_GST = data.get("total_amount_with_GST", purchase.total_amount_with_GST)

            purchase.save()

            # Update purchase items
            items = data.get("purchase_items", [])

            # Delete existing items and add new ones
            existing_items = PurchaseItem.objects.filter(purchase=purchase)
            for item in existing_items:
                stock_item = MedicineStock.objects.filter(
                    ref_user=request.user, batch=item.batch,
                ).first()
                if stock_item:
                    stock_item.qty -= item.qty  # Reduce stock by previous qty
                    stock_item.save()

            # Delete existing purchase items
            existing_items.delete()

            for item in items:
                PurchaseItem.objects.create(
                    purchase=purchase,
                    company=item.get("Company"),
                    item_name=item.get("ItemName"),
                    batch=item.get("Batch"),
                    exp_date=item.get("ExpDate"),
                    mrp=item.get("MRP"),
                    rate=item.get("Rate"),
                    qty=item.get("Qty"),
                    total=item.get("Total"),
                    cgst=item.get("cgst"),
                    sgst=item.get("sgst"),
                    totalGSTamount=item.get("totalGSTamount"),
                    totalWithGST=item.get("totalWithGST"),
                )
                
                # Update or create stock
                stock, created = MedicineStock.objects.get_or_create(
                    ref_user=request.user,
                    batch=item["Batch"],
                    defaults={
                        "company": item["Company"],
                        "item_name": item["ItemName"],
                        "exp_date": datetime.strptime(item.get("ExpDate"), "%Y-%m-%d").date() if item.get("ExpDate") else None,
                        "qty": item["Qty"],
                        "mrp": item["MRP"],
                        "rate": item["Rate"],
                        "cgst": item["cgst"],
                        "sgst": item["sgst"],
                        "total": item["Total"],
                        "totalGSTamount": item["totalGSTamount"],
                        "totalWithGST": item["totalWithGST"],
                    }
                )

                if not created:
                    # If stock exists, update quantity and expiration date
                    stock.qty = F("qty") + item["Qty"]
                    stock.exp_date = datetime.strptime(item.get("ExpDate"), "%Y-%m-%d").date() if item.get("ExpDate") else None
                    stock.save()


            return JsonResponse({"success": True, "message": "Purchase updated successfully", "purchase_invoice_number":purchase.purchase_invoice_number})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def delete_purchase(request, purchase_id):
    if request.method == "DELETE" and request.user.is_authenticated:
        try:
            purchase = Purchase.objects.get(purchase_invoice_number=purchase_id)
            purchase.delete()
            return JsonResponse({"success": True, "message": "Purchase deleted successfully!"})
        except Purchase.DoesNotExist:
            return JsonResponse({"success": False, "message": "Purchase not found!"}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request!"}, status=400)

@csrf_exempt  # Use this only if your frontend is not sending CSRF tokens (not recommended for production).
# @login_required  # Ensure the user is authenticated.
def add_party(request):
    """
    API endpoint to add a new party. Handles JSON requests from the frontend.
    """
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # Parse the JSON data
            data = json.loads(request.body)

            # Extract fields
            name = data.get('name')
            contact_number = data.get('contact_number')
            email = data.get('email', None)
            gst_number = data.get('gst_number', None)
            address = data.get('address', None)
            ref_user = request.user.username

            # Validate required fields
            if not name or not contact_number:
                return JsonResponse({'error': 'Name and Contact Number are required.'}, status=400)
            
            # Create a new Party object
            party = Party.objects.create(
                user_details=UserDetails.objects.get(user=User.objects.get(username=request.user.username)),
                name=name,
                contact_number=contact_number,
                email=email,
                gst_number=gst_number,
                address=address,
                ref_user=ref_user
            )

            # Success response
            return JsonResponse({'message': 'Party added successfully.', 'party_id': party.party_id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)


@csrf_exempt  # Remove in production if CSRF token is implemented
# @login_required
def edit_party(request, party_id):
    """
    API endpoint to edit an existing party.
    """
    if request.method == 'PUT' and request.user.is_authenticated:
        try:
            # Parse the JSON data
            data = json.loads(request.body)

            # Fetch the Party instance
            party = get_object_or_404(Party, pk=party_id, user_details=UserDetails.objects.get(user=User.objects.get(username=request.user.username)))

            # Update fields if present
            party.name = data.get('name', party.name)
            party.contact_number = data.get('contact_number', party.contact_number)
            party.email = data.get('email', party.email)
            party.gst_number = data.get('gst_number', party.gst_number)
            party.address = data.get('address', party.address)
            party.save()

            # Success response
            return JsonResponse({'message': 'Party updated successfully.', "party_id":party.party_id}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    return JsonResponse({'error': 'Invalid request method. Only PUT is allowed.'}, status=405)

@csrf_exempt  # Remove in production if CSRF token is implemented
# @login_required
def delete_party(request, party_id):
    """
    API endpoint to delete an existing party.
    """
    if request.method == 'DELETE' and request.user.is_authenticated:
        # Fetch the Party instance
        party = get_object_or_404(Party, pk=party_id, user_details=UserDetails.objects.get(user=User.objects.get(username=request.user.username)))

        # Delete the party
        party.delete()

        # Success response
        return JsonResponse({'message': 'Party deleted successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method. Only DELETE is allowed.'}, status=405)

# @csrf_exempt
# def save_purchase(request):
    
def test(request):
    return render(request, "test.html")



@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        mode = request.GET.get("hub.mode")
        challenge = request.GET.get("hub.challenge")
        verify_token = request.GET.get("hub.verify_token")
        
        if mode and verify_token:
            if mode == "subscribe" and verify_token == mytoken:
                return HttpResponse(challenge, status=200)
            else:
                return HttpResponse(status=403)

        return HttpResponse(status=400)

    if request.method == 'POST':
        body_param = json.loads(request.body.decode('utf-8'))

        if body_param:
            if (body_param.get("entry") and 
                body_param["entry"][0].get("changes") and 
                body_param["entry"][0]["changes"][0].get("value") and 
                body_param["entry"][0]["changes"][0]["value"].get("messages") and 
                body_param["entry"][0]["changes"][0]["value"]["messages"][0]):

                phone_number_id = body_param["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
                from_ = body_param["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
                msg_body = body_param["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

                # print(f"Phone number ID: {phone_number_id}")
                # print(f"From: {from_}")
                # print(f"Message body: {msg_body}")

                whatsappcloud.sendText(f"From: {from_}\nMessage: {msg_body}", "919091467852")
                return HttpResponse(status=200)

            return HttpResponse(status=404)
    return HttpResponse(status=405)
    

def download_invoice_pdf(request, purchase_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User authentication required"}, status=401)
    try:
        # Fetch the purchase details from the database
        purchase = Purchase.objects.get(purchase_invoice_number=purchase_id)
        items = PurchaseItem.objects.filter(purchase=purchase)  # Assuming a related model for invoice items

        # Prepare data for rendering
        context = {
            "invoice": purchase,
            "items": items,
        }

        # Load the HTML template
        template = get_template("purchase_invoice_template.html")
        html = template.render(context)

        # Create PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="invoice{purchase_id}_{purchase.Supplier_name}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse("We had some errors generating the PDF", status=500)
        return response

    except Purchase.DoesNotExist:
        return HttpResponse("Invoice not found", status=404)


def download_sales_invoice_pdf(request, invoice_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User authentication required"}, status=401)
    try:
        # Fetch the billing details from the database
        billing = Billing.objects.get(invoice_number=invoice_id)
        items = BillingItem.objects.filter(billing=billing)  # Get related billing items

        # Prepare data for rendering
        context = {
            "invoice": billing,
            "items": items,
        }

        # Load the HTML template
        template = get_template("sales_invoice_template.html")  # Create this template
        html = template.render(context)

        # Create PDF response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="SalesInvoice_{invoice_id}_{billing.customer_name}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse("We had some errors generating the PDF", status=500)
        return response

    except Billing.DoesNotExist:
        return HttpResponse("Invoice not found", status=404)
    


def generate_invoice_pdf(request, purchase_id):
    print("Hi.........")
    t1 = threading.Thread(target=extrafunction.deletExtraImages)
    t1.start()
    try:
        # Fetch the purchase details from the database
        purchase = Purchase.objects.get(purchase_invoice_number=purchase_id)
        items = PurchaseItem.objects.filter(purchase=purchase)  # Assuming a related model for invoice items

        # Prepare data for rendering
        context = {
            "invoice": purchase,
            "items": items,
        }
        # Load HTML template
        template = get_template("purchase_invoice_template.html")
        html = template.render(context)

        # Create a BytesIO buffer to hold the PDF data
        # pdf_buffer = BytesIO()

        # pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
        fileName = f"./media/FileDBFolder/testPdf-{23569}.pdf"
        print(fileName)

        with open(fileName, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        

        

        # if pisa_status.err:
        #     return None, "Error generating PDF"
        
        # Seek to the beginning of the BytesIO buffer
        # pdf_buffer.seek(0)

        # Create a FileResponse with the generated PDF
        # response = FileResponse(pdf_buffer, as_attachment=True, filename=f"invoice_{purchase.purchase_invoice_number}.pdf")
        
        return HttpResponse("Working...")

    except Exception as e:
        return None, str(e)
    
def get_medicine_stock(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User authentication required"}, status=401)
    if request.method == "GET":
        try:
            stock_items = MedicineStock.objects.filter(ref_user=request.user.username).values(
                "item_name", "batch", "mrp", "qty"
            )
            return JsonResponse(list(stock_items), safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_customers(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User authentication required"}, status=401)
    
    if request.method == "GET":
        try:
            customers = Customer.objects.filter(ref_user=request.user.username).values(
                "customer_id", "name", "phone_number"
            )

            customer_list = [
                {"customerId": c["customer_id"], "name": c["name"], "phone": c["phone_number"]}
                for c in customers
            ]

            return JsonResponse(customer_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)