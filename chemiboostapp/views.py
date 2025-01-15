from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chemiboostapp import whatsappcloud
from django.contrib.auth.decorators import login_required
from chemiboostapp.models import Party, UserDetails
from django.core import serializers

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
    
