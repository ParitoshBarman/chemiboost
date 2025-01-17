from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chemiboostapp import whatsappcloud
from django.contrib.auth.decorators import login_required
from chemiboostapp.models import Party, UserDetails, Purchase, PurchaseItem
from django.core import serializers
from datetime import datetime
from django.core.paginator import Paginator

mytoken = "hjhhkjhjhkjhjkghghjgjhghg"

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
    return render(request, "stock.html")
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
                    "Total": item.total
                }
                for item in purchase_items
            ]

            purchases_data.append({
                "id": purchase.pk,
                "Supplier_name": purchase.Supplier_name,
                "Supplier_contact_number": purchase.Supplier_contact_number,
                "purchase_date": purchase.purchase_date.strftime("%Y-%m-%d"),
                "total_amount": purchase.total_amount,
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
                )

            return JsonResponse({"message": "Purchase created successfully!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_purchase(request, purchase_id):
    if request.method == "DELETE":
        try:
            purchase = Purchase.objects.get(id=purchase_id)
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
    
