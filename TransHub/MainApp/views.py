from collections import UserDict
import json
from msilib.schema import ListView
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import BRAND_CHOICES, CATEGORY, Bus, Category, Location, Payment, Schedule, Users,Seat_map,Address,Supplier,Stock, Warehouse,WarehouseType,StorageMapDup
from TransHub.settings import EMAIL_HOST_USER
from .models import Users
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib import messages
from .models import Users, UserProfile
from datetime import datetime
from .models import Booking
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
# from django.http import HttpResponse

@never_cache
def showIndex(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@csrf_protect
def SignUp(request):
    if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST.get('phone')
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            role='user'
            
            if password != confirm_password:
                 return render(request, SignUp.html)
            user = Users(username=username,phone_number=phone, email=email,role=role)
            # password set
            user.set_password(password)
            #save the user to database
            user.save()
            UserProfile.objects.create(user=user)
            
            subject = 'Hello, '+username
            message = 'Your registration has been Successfully completed'
            from_email = EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('login')
            
    return render(request,'SignUp.html')

# def Log(request):
#     if request.method == "POST":
#          username = request.POST['username']
#          user_password = request.POST['password']
#          user = authenticate(username=username, password=user_password)
#          if user is not None:
#             if user.is_superuser:
#                 login(request, user)
#                 request.session['username'] = username
#                 return redirect("Admin_Home")     
#             login(request, user)
#             return redirect('Home')
#          else:
#               return render(request, 'login.html', {'Error_message': 'invalid creadential!!'})
    
#     return render(request,'login.html')


from django.contrib import messages

def Log(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("User role:", user.role)  # Print user role for debugging
            if user.is_superuser:
                login(request, user)
                request.session['username'] = username
                return redirect("Admin_Home")
            elif user.role == 'Warehouse':
                print("Redirecting to index1")  # Print debug message
                login(request, user)
                request.session['username'] = username
                return redirect("index1")
            else:
                login(request, user)
                request.session['username'] = username
                return redirect('Home')
        else:
            # Invalid username or password
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

# def Log(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         user_password = request.POST.get('password')
#         user = authenticate(username=username, password=user_password)
#         if user is not None:
#             if user.is_superuser:
#                 login(request, user)
#                 request.session['username'] = username
#                 return redirect("Admin_Home")
#             else:
#                 request.session['username'] = username
#                 login(request, user)
#                 if user.role == 'WAREHOUSE':
#                     return redirect('warehouselogin')
#                 else:
#                     return redirect('Home')
#         else:
#             return render(request, 'login.html', {'Error_message': 'Invalid credentials!!'})
#     else:
#         return render(request, 'login.html')  # Return login page for GET requests

    
def logout_user(request):
     if request.user.is_authenticated:
          logout(request)
     return redirect('showindex')   

import random
def generateOTP():
     generatedOTP = "".join(str(random.randint(0, 9)) for _ in range(6))
     return generatedOTP


#@login_required(login_url='login')
@never_cache
def Home(request):
     return render(request, 'home.html')

def validateGlobalEmail(request):
     email = request.GET['email']
     cpnm = "TransHub Corp. Ltd."
     otp = generateOTP()
     subject = 'Hello, Django Email!'
     message = 'Here is Your OTP.'+otp
     from_email = EMAIL_HOST_USER
     recipient_list = [email] 
     data = {
          "exists": send_mail(subject, message, f"{cpnm} <{from_email}>", recipient_list),
          "otp": otp
     }
     return JsonResponse(data)


def check_username(request):
     username = request.GET.get('username', '')
     user_exits = Users.objects.filter(username=username).exists()
     return JsonResponse({'exists': user_exits})

def check_email(request):
     email = request.GET.get('email', '').lower
     email_exists = Users.objects.filter(email=email).exists()
     return JsonResponse({'exists': email_exists})

def Staff_signUp(request):
    if request.method == 'POST':
        # Similar to the SignUp view, include the role field
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST.get('phone')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = 'Staff'  # Set the role to 'staff' for staff registration

        if password != confirm_password:
            return render(request, 'StaffSignUp.html')

        user = Users(username=username, phone_number=phone, email=email, role=role)
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'StaffSignUp.html')

@never_cache
def Admin_Home(request):
     if not request.user.is_authenticated:
         return redirect ('login')
     return render(request, 'adminhome.html')

def user_account(request):
    role_filter = request.GET.get('role')
    users = Users.objects.filter(~Q(is_superuser=True))  # Exclude superusers by default

    if role_filter:
        users = users.filter(role=role_filter)

    context = {'User_profiles': users, 'role_filter': role_filter}
    return render(request, 'usertable.html', context)

from django.template.loader import render_to_string
from django.utils.html import strip_tags


#def ActivateAccount(request):
#     return render(request, 'activate.html')

def activate_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)

    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, f"User '{user.username}' has been activated by the admin, and an email has been sent.")
        
        # Send activation email to the user
        subject = "Account Activation"
        html_message = render_to_string('activation_email.html', {'user': user})
        plain_message = strip_tags(html_message)
        from_email = "transhubcorporationltd@gmail.com"  # Update with your email
        recipient_list = [user.email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

    else:
        messages.warning(request, f"User '{user.username}' is activated.")

    return redirect('user_account')


def activatation_email(request):
     return render(request, 'activation_email.html')

def deactivate_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()

        # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'transhubcorporationltd@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is deactivated.")
    return redirect('user_account')

def deactivation_email(request):
     return render(request, 'deactivation_email.html')

# views.py
# views.py
from django.shortcuts import render, redirect
from .forms import SaveBus, SaveCategory, SaveLocation, SaveSchedule, SupplierForm, UserProfileForm, AdditionalProfileForm

def update_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    try:
        user = Users.objects.get(username=request.user.username)
    except Users.DoesNotExist:
        user = None

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        date_of_birth = request.POST.get('date_of_birth')
        profile_picture = request.FILES.get('profile_picture')  # Updated this line

        # Additional validation if needed
        # ...

        # Update Users fields
        user.phone_number = phone_number
        user.save()

        # Update UserProfile fields
        user_profile.age = age
        user_profile.gender = gender
        user_profile.city = city
        user_profile.date_of_birth = date_of_birth
        if profile_picture:
            user_profile.profile_picture = profile_picture  # Updated this line

        user_profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'update_profile.html', {'user_profile': user_profile, 'user': user})




def profile(request):
    return render(request, 'profile.html')

#context text
context = {
    'page_title' : 'File Management System',
}

#category
@login_required
def category_mgt(request):
    context['page_title'] = "Bus Categories"
    categories = Category.objects.all()
    context['categories'] = categories

    return render(request, 'category_mgt.html', context)

#save_category
@login_required
def save_category(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            category = Category.objects.get(pk=request.POST['id'])
        else:
            category = None
        if category is None:
            form = SaveCategory(request.POST)
        else:
            form = SaveCategory(request.POST, instance= category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

#manage_category
@login_required
def manage_category(request, pk=None):
    context['page_title'] = "Manage Category"
    if not pk is None:
        category = Category.objects.get(id = pk)
        context['category'] = category
    else:
        context['category'] = {}

    return render(request, 'manage_category.html', context)

#delete_category
@login_required
def delete_category(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            category = Category.objects.get(id = request.POST['id'])
            category.delete()
            messages.success(request, 'Category has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Category has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Category has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Location
@login_required
def location_mgt(request):
    context['page_title'] = "Locations"
    locations = Location.objects.all()
    context['locations'] = locations

    return render(request, 'location_mgt.html', context)

#save location
@login_required
def save_location(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            location = Location.objects.get(pk=request.POST['id'])
        else:
            location = None
        if location is None:
            form = SaveLocation(request.POST)
        else:
            form = SaveLocation(request.POST, instance= location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

#manage location
@login_required
def manage_location(request, pk=None):
    context['page_title'] = "Manage Location"
    if not pk is None:
        location = Location.objects.get(id = pk)
        context['location'] = location
    else:
        context['location'] = {}

    return render(request, 'manage_location.html', context)

#delete location
@login_required 
def delete_location(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            location = Location.objects.get(id = request.POST['id'])
            location.delete()
            messages.success(request, 'Location has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'location has failed to delete'
            print(err)

    else:
        resp['msg'] = 'location has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

# bus
@login_required
def bus_mgt(request):
    context['page_title'] = "Buses"
    buses = Bus.objects.all()
    context['buses'] = buses

    return render(request, 'bus_mgt.html', context) 

@login_required
def save_bus(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            bus = Bus.objects.get(pk=request.POST['id'])
        else:
            bus = None
        if bus is None:
            form = SaveBus(request.POST)
        else:
            form = SaveBus(request.POST, instance= bus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def manage_bus(request, pk=None):
    context['page_title'] = "Manage Bus"
    categories = Category.objects.filter(status = 1).all()
    context['categories'] = categories
    if not pk is None:
        bus = Bus.objects.get(id = pk)
        context['bus'] = bus
    else:
        context['bus'] = {}

    return render(request, 'manage_bus.html', context)

@login_required
def delete_bus(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            bus = Bus.objects.get(id = request.POST['id'])
            bus.delete()
            messages.success(request, 'Bus has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'bus has failed to delete'
            print(err)

    else:
        resp['msg'] = 'bus has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

# schedule
@login_required
def schedule_mgt(request):
    context['page_title'] = "Trip Schedules"
    schedules = Schedule.objects.all()
    context['schedules'] = schedules

    return render(request, 'schedule_mgt.html', context)

@login_required
def save_schedule(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            schedule = Schedule.objects.get(pk=request.POST['id'])
        else:
            schedule = None
        if schedule is None:
            form = SaveSchedule(request.POST)
        else:
            form = SaveSchedule(request.POST, instance= schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def manage_schedule(request, pk=None):
    context['page_title'] = "Manage Schedule"
    buses = Bus.objects.filter(status = 1).all()
    locations = Location.objects.filter(status = 1).all()
    context['buses'] = buses
    context['locations'] = locations
    if not pk is None:
        schedule = Schedule.objects.get(id = pk)
        context['schedule'] = schedule
    else:
        context['schedule'] = {}

    return render(request, 'manage_schedule.html', context)

@login_required
def delete_schedule(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            schedule = Schedule.objects.get(id = request.POST['id'])
            schedule.delete()
            messages.success(request, 'Schedule has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'schedule has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Schedule has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json") 


class Seat:
    def __init__(self, number, is_reserved, is_women_seat):
        self.number = number
        self.is_reserved = is_reserved
        self.is_women_seat = is_women_seat

def bus_seat_map(request):
    # Example: Creating a list of 40 seats with alternating reserved and available status,
    # and 5 women seats
    num_seats = 40
    num_women_seats = 5
    seats = [Seat(number=i, is_reserved=i % 2 == 0, is_women_seat=i < num_women_seats) for i in range(1, num_seats + 1)]

    return render(request, 'bus_grid_seat.html', {'seats': seats})

def book_seat(request):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats')
        # Handle booking logic here
        return HttpResponse(f'Selected Seats: {", ".join(selected_seats)}')
    else:
        return HttpResponse('Invalid request method')


# find trip set

from django.shortcuts import render
from django.http import Http404
from datetime import datetime
from .models import Location, Schedule

from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from .models import Schedule, Location

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Schedule, Location

from django.shortcuts import render, Http404, HttpResponseRedirect, reverse
from django.utils import timezone
from .models import Schedule, Location

def find_trip(request):
    context = {}
    context['page_title'] = 'Find Trip Schedule'
    context['locations'] = Location.objects.filter(status=1).all()
    today = timezone.now().strftime("%Y-%m-%d")
    context['today'] = today

    if request.method == 'GET':
        depart = request.GET.get('depart')
        destination = request.GET.get('destination')
        journey_date = request.GET.get('journeyDate')
        return_date = request.GET.get('returnDate')

        # Basic input validation
        if not depart and not destination and not journey_date:
            context['error_message'] = 'Please provide at least one search parameter.'
            return render(request, 'find_trip.html', context)

        # Additional validation can be added here if needed

        # Validate depart and destination locations
        try:
            depart_location = Location.objects.get(pk=depart)
        except Location.DoesNotExist:
            raise Http404('Depart location does not exist')

        try:
            destination_location = Location.objects.get(pk=destination)
        except Location.DoesNotExist:
            raise Http404('Destination location does not exist')

        # Query Schedule model based on search parameters
        schedules = Schedule.objects.all()

        if depart:
            schedules = schedules.filter(depart=depart_location)
        if destination:
            schedules = schedules.filter(destination=destination_location)
        if journey_date:
            try:
                journey_date = timezone.datetime.strptime(journey_date, '%Y-%m-%d').date()
            except ValueError:
                context['error_message'] = 'Invalid journey date format.'
                return render(request, 'find_trip.html', context)

            # Filter schedules for the selected journey_date
            schedules = schedules.filter(date_created__contains=journey_date)

        if schedules.exists():
            schedule_code = schedules.first().code
            return HttpResponseRedirect(reverse('schedule_view_page', kwargs={'journey_date': journey_date}))

        context['schedules'] = schedules

        # Render the schedule_view_page template with the filtered schedules
        return render(request, 'schedule_view_page.html', context)

    return render(request, 'find_trip.html', context)

from django.utils import timezone

from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from .models import Schedule, Location

from django.shortcuts import render, Http404
from django.utils import timezone
from .models import Schedule

def schedule_view_page(request, journey_date):
    context = {}

    if request.method == 'GET':
        depart = request.GET.get('depart')
        destination = request.GET.get('destination')

        # Validate journey_date format
        try:
            journey_date = timezone.datetime.strptime(journey_date, '%Y-%m-%d').date()
        except ValueError:
            raise Http404('Invalid journey date format.')

        # Filter schedules based on the user's search parameters
        schedules = Schedule.objects.filter(schedule__date=journey_date)

        if depart:
            schedules = schedules.filter(depart__location__icontains=depart)

        if destination:
            schedules = schedules.filter(destination__location__icontains=destination)

        # Check if any schedules match the search criteria
        if schedules.exists():
            context['schedules'] = schedules
        else:
            context['no_schedules_found'] = True

    return render(request, 'schedule_view_page.html', context)




from django.shortcuts import render, redirect
from .models import Feedback
from django.contrib.auth.decorators import login_required

@never_cache
@login_required(login_url="login")
def submit_feedback(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        if feedback_message:
            Feedback.objects.create(User=request.user, message=feedback_message)
            # You can add additional logic here (e.g., sending a confirmation email)
            return redirect('feedback_thankyou')

    return render(request, 'feedback_form.html')


def feedback_thankyou(request):
     return render(request,'feedback_thankyou.html')


from django.shortcuts import render
from .models import Feedback

def adminfeedback(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'adminfeedback.html', {'feedback_list': feedback_list})

# from .models import Booking

def seat_reservation(request, schedule_code, schedule_id):
    user = request.user
    user_profile = user.userprofile
    
    # Assuming schedule_code is used to identify the schedule
    bookings_count = Booking.objects.filter(schedule__code=schedule_code).count()
    
    context = {
        'user_profile': user_profile,
        'bookings_count': bookings_count,
        'bus_id': schedule_id,
        'schedule_code': schedule_code
        # Other context variables for bus seat reservation
        # ...
    }
    return render(request, 'seat_reservation.html', context)

from django.http import JsonResponse
# from .models import Booking

def create_booking(request):
    if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Extract the selected seat count from the AJAX request
        selected_seat_count = int(request.POST.get('selectedSeatCount'))
        
        # Create a booking object with the count of selected seats
        booking = Booking.objects.create(
            seat_no_count=selected_seat_count
            # You can add other fields here if needed
        )
        # Save the booking object
        booking.save()
        
        return JsonResponse({'message': 'Booking successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
from django.http import JsonResponse
# from .models import Booking

def create_booking(request):
    if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        selected_seat_count = int(request.POST.get('selectedSeatCount', 0))
        # Perform any operation you want with the selected seat count here
        # For example, saving it to the database
        booking = Booking.objects.create(seat_no_count=selected_seat_count)
        booking.save()
        return JsonResponse({'message': 'Booking successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Schedule

from django.shortcuts import render

# views.py
from django.shortcuts import render, redirect
# from .models import Booking  # Import the Booking model

from django.shortcuts import render, redirect
# from .models import Booking
from django.shortcuts import render, redirect
# from .models import Booking
from django.shortcuts import render, redirect
# from .models import Booking
from django.shortcuts import render, redirect
# from .models import Booking
from django.shortcuts import render, redirect
# from .models import Booking

from django.shortcuts import render, redirect
# from .models import Booking


from django.http import JsonResponse

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json

def seatReservation(request):
    if request.method == 'POST':
        data_list_json = request.POST.get('data_list')
        bus_Id = int(request.POST['bus_id'])
        schedule_Id = int(request.POST['schedule_code'])

        bus = Bus.objects.get(pk=bus_Id)
        schedule = Schedule.objects.get(code=schedule_Id) 
        
        # Check if data_list_json is not empty or None
        if data_list_json:
            data_list = json.loads(data_list_json)
            print(data_list)
            
            # Assuming Seat_map is your Django model
            if data_list:  # Check if data_list is not empty
                for i in data_list:
                    seatMap = Seat_map()
                    seatMap.seat_number = i 
                    seatMap.bus =  bus # FK
                    seatMap.schedule =  schedule # FK
                    seatMap.booked_by = request.user
                    seatMap.save()

                return redirect("passengers")  # Redirect to passengers page if at least one seat is selected
            else:
                error_message = 'No seats selected'
                return render(request, 'seat_reservation.html', {'error_message': error_message})  # Render the same page with an error message
        else:
            error_message = 'No data received'
            return render(request, 'seat_reservation.html', {'error_message': error_message})  # Render the same page with an error message
    else:
        return HttpResponse("no data found")
 
from django.views.decorators.csrf import csrf_exempt
import razorpay

@csrf_exempt
def passengers(request):
    seatMap = Seat_map.objects.filter(booked_by_id=request.user.id)
    total_amount=0
    for i in seatMap:
        total_amount += i.schedule.fare
    context = {
        "seatMap": seatMap,
        "total_amount": total_amount,
        "order_id": False
    }
    if request.method == 'POST':
        for i in seatMap:
            name = request.POST[f"name{i.seat_number}"]
            
        return HttpResponse(name)
    else:
        client = razorpay.Client(auth=("rzp_test_KF3ZUR5Voabs80", "uC4UBn0BEqHG6IqqECWD74gL"))     

        data_info = {
            "amount": 50000,
            "currency": "INR",
            "receipt": "receipt#1",
            "partial_payment": False,
            "notes": {
                "key1": "value3",
                "key2": "value2"
                }  
        }
        payment = client.order.create(data=data_info)
        context['order_id'] = payment['id']

        return render(request, 'passengers.html', context)  # Render the form page for GET requests



def payments_view(request):
    return render(request, 'payments.html')

def index1(request):
    return render(request, 'index1.html')

def warehouseindex(request):
    return render(request, 'warehouseindex.html')

def warehouse_signup_page(request):
    if request.method == 'POST':
        # Extract user registration data from the form
        username = request.POST.get('fullname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        address = request.POST.get('address')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password == confirm_password:
            # Create the user instance
            user = Users.objects.create_user(username=username, email=email, password=password,phone_number=phone_number,role='Warehouse')
            
          

            # Create the address instance
            user_address = Address.objects.create(
                user=user,
                address=address,
                street=street,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code
            )


            user.save()
           
            user_address.save()

            # No need to call save() on user, profile, and user_address separately,
            # since create() method already saves the instances to the database

            # Redirect to a success page or any other page
            return redirect('login')
        else:
            # Passwords don't match, handle accordingly (e.g., show an error message)
            # For simplicity, let's just return a HttpResponse with an error message
            return HttpResponse('Passwords do not match')
    else:
        # Render the registration form
        return render(request, 'warehouseregister.html')

def terms_and_condition(request):
    return render(request, 'terms_and_condition.html')

def warehouse_login_page(request):
    return render(request, 'warehouselogin.html')

from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def warehouse_profile_page(request):
    user = request.user
    if request.method == 'POST':
        if 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password1')
            repeat_password = request.POST.get('new_password2')

            if check_password(current_password, user.password):
                if new_password == repeat_password:
                    user.set_password(new_password)
                    user.save()
                    return redirect('warehouse_profile_page')
                else:
                    error_message = "New password and repeat password do not match."
            else:
                error_message = "Current password is incorrect."

            context = {
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'error_message': error_message
            }
            return render(request, 'warehouseprofile.html', context)
        elif 'username' in request.POST or 'email' in request.POST or 'phone_number' in request.POST:
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone_number = request.POST.get('phone_number')
            user.save()
            return redirect('warehouse_profile_page')
    else:
        context = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number
        }
        return render(request, 'warehouseprofile.html', context)

def drop_down(request):
    return render(request, "dropdownpage.html")

def admin_warehouse(request):
    return render(request,  "admin_warehouse.html")


def warehouse_details(request):
    return render(request, "warehouse_details.html")

def warehouse_staff(request):
    return render(request, "warehouse_staff.html")

def warehouse_orders(request):
    return render(request, "warehouse_orders.html")

def warehouse_products(request):
    return render(request, "warehouse_products.html")

# for inventory purpose
def inventory_view(request):
    stocks = Stock.objects.filter(is_deleted=False)
    context = {'stocks': stocks,
               'CATEGORY': CATEGORY,
               'BRAND_CHOICES': BRAND_CHOICES,
               }
    return render(request, 'inventory_view.html', context)

def generate_unique_sku(sku):
    # Logic to generate a unique SKU if it already exists
    # For example, you might append a number to make it unique
    # Here's a simple example using slugify to generate a unique SKU
    return slugify(sku)

def add_stock(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        quantity = request.POST.get('quantity')
        cost_price = request.POST.get('costPrice')
        image = request.FILES.get('image')
        date_added = request.POST.get('dateAdded')
        description = request.POST.get('description') 

        # Generate a unique SKU if not provided by the user
        sku = request.POST.get('sku') or slugify(name)  # Example of generating SKU from name
        
        # Ensure the generated SKU is unique
        while Stock.objects.filter(sku=sku).exists():
            # If the SKU already exists, modify it to make it unique
            sku += '-1'  # You might want to modify this logic based on your requirements

        stock = Stock(name=name, category=category, brand=brand, quantity=quantity,
                      costPrice=cost_price, image=image, dateAdded=date_added, sku=sku, description=description)
        stock.save()
        return redirect('inventory_view')
    else:
        return HttpResponse('Method Not Allowed')

def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.name = request.POST.get('name', stock.name)
        stock.category = request.POST.get('category', stock.category)
        stock.brand = request.POST.get('brand', stock.brand)
        stock.quantity = request.POST.get('quantity', stock.quantity)
        stock.costPrice = request.POST.get('costPrice', stock.costPrice)
        if 'image' in request.FILES:
            stock.image = request.FILES['image']
        stock.dateAdded = request.POST.get('dateAdded', stock.dateAdded)
        stock.description = request.POST.get('description', stock.description)
        stock.save()
        return redirect('inventory_view')
    context = {'stock': stock}
    return render(request, 'edit_stock.html', context)

def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    stock.is_deleted = True
    stock.save()
    return redirect('inventory_view')

def add_stock_page(request):
    # Render the add stock modal form
    return render(request, 'add_stock.html')

def edit_stock_page(request, stock_id):
    # Render the edit stock modal form
    stock = get_object_or_404(Stock, pk=stock_id)
    context = {'stock': stock}
    return render(request, 'edit_stock.html', context)

def get_stock_details(request):
    if request.method == 'GET' and 'stock_id' in request.GET:
        stock_id = request.GET.get('stock_id')
        try:
            stock = Stock.objects.get(id=stock_id)
            # Construct JSON response with stock details
            data = {
                'name': stock.name,
                'description': stock.description,
                'quantity': stock.quantity,
                'cost_price': str(stock.costPrice),  # Convert DecimalField to string
                'date_added': stock.dateAdded.strftime('%Y-%m-%d'),  # Format date as string
                'image_url': stock.image.url,  # Assuming 'image' is an ImageField
            }
            return JsonResponse(data)
        except Stock.DoesNotExist:
            return JsonResponse({'error': 'Stock not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

# # shows a lists of all suppliers
# class SupplierListView(ListView):
#     model = Supplier
#     template_name = "suppliers_list.html"
#     queryset = Supplier.objects.filter(is_deleted=False)
#     paginate_by = 10


# # used to add a new supplier
# class SupplierCreateView(SuccessMessageMixin, CreateView):
#     model = Supplier
#     form_class = SupplierForm
#     success_url = ''
#     success_message = "Supplier has been created successfully"
#     template_name = "edit_supplier.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'New Supplier'
#         context["savebtn"] = 'Add Supplier'
#         return context     


# # used to update a supplier's info
# class SupplierUpdateView(SuccessMessageMixin, UpdateView):
#     model = Supplier
#     form_class = SupplierForm
#     success_url = ''
#     success_message = "Supplier details has been updated successfully"
#     template_name = "edit_supplier.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Edit Supplier'
#         context["savebtn"] = 'Save Changes'
#         context["delbtn"] = 'Delete Supplier'
#         return context


# # used to delete a supplier
# class SupplierDeleteView(View):
#     template_name = "delete_supplier.html"
#     success_message = "Supplier has been deleted successfully"

#     def get(self, request, pk):
#         supplier = get_object_or_404(Supplier, pk=pk)
#         return render(request, self.template_name, {'object' : supplier})

#     def post(self, request, pk):  
#         supplier = get_object_or_404(Supplier, pk=pk)
#         supplier.is_deleted = True
#         supplier.save()                                               
#         messages.success(request, self.success_message)
#         return redirect('suppliers-list')


# # used to view a supplier's profile
# class SupplierView(View):
#     def get(self, request, name):
#         supplierobj = get_object_or_404(Supplier, name=name)
#         bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
#         page = request.GET.get('page', 1)
#         paginator = Paginator(bill_list, 10)
#         try:
#             bills = paginator.page(page)
#         except PageNotAnInteger:
#             bills = paginator.page(1)
#         except EmptyPage:
#             bills = paginator.page(paginator.num_pages)
#         context = {
#             'supplier'  : supplierobj,
#             'bills'     : bills
#         }
#         return render(request, 'supplier.html', context)
    

def supplier_page(request):
    return render(request, "supplier/supplier_page.html") 

def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Supplier.objects.filter(name=name).exists():
            messages.error(request, 'Supplier with this name already exists.')
        # Retrieving form data:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        gstin = request.POST.get('gstin')

        # Creating a new Supplier object and saving it to the database:
        supplier = Supplier(name=name, phone=phone, address=address, email=email, gstin=gstin)
        supplier.save()
        messages.success(request, 'wait for admin approve!')

        # Redirecting to the supplier_page (make sure to define the URL name 'supplier_page' in your urls.py)
        return redirect('supplier_page')
    else:
        # If not a POST request, just show the form page again (or you could direct to a different page)
        return render(request, 'supplier/add_supplier.html')  # Replace 'your_form_template.html' with your actual form template
    

def request_accepting_page(request):
    # Retrieve only pending supplier requests
    pending_suppliers = Supplier.objects.filter(status='pending')
    return render(request, 'supplier/request_accepting_page.html', {'suppliers': pending_suppliers})

def accept_supplier(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.status = '1'  # '1' corresponds to "Accept" in your STATUS_CHOICES
        supplier.save()

        # Send email notification
        send_mail(
            'Supplier Request Approved',
            'Your supplier request has been approved.',
            'transhubcorporationltd@gmail.com',  # Change this to your admin email address
            [supplier.email],
            fail_silently=False,
        )

    return redirect('request_accepting_page')

def reject_supplier(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.status = '3'  # '3' corresponds to "Reject" in your STATUS_CHOICES
        supplier.save()

        # Send email notification
        send_mail(
            'Supplier Request Rejected',
            'Your supplier request has been rejected by the admin.',
            'transhubcorporationltd@gmail.com',  # Change this to your admin email address
            [supplier.email],
            fail_silently=False,
        )

    return redirect('request_accepting_page')


def sale_stock(request):
    return render(request, 'purchases/sale_stock.html')

def new_purchase(request):
    return render(request, 'purchases/new_purchase.html')

#warehouse
def supplier_selection(request):
    suppliers = Supplier.objects.all()
    return render(request, 'purchases/supplier_selection.html', {'suppliers': suppliers, 'selected_supplier': None})

def new_purchase(request):
    if request.method == 'POST':
        selected_supplier_id = request.POST.get('supplier')
        selected_supplier = get_object_or_404(Supplier, id=selected_supplier_id)
        stock_items = Stock.objects.filter(supplier=selected_supplier)
        return render(request, 'purchases/new_purchase.html', {'selected_supplier': selected_supplier, 'stock_items': stock_items})
    else:
        return redirect('supplier_selection')
    

#warehouse
def warehouse_view(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse/warehouse_views.html', {'warehouses': warehouses})

def add_warehouse(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        total_capacity = request.POST.get('total_capacity')
        available_capacity = request.POST.get('available_capacity')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_email = request.POST.get('contact_person_email')
        contact_person_phone = request.POST.get('contact_person_phone')
        status = request.POST.get('status')
        date = request.POST.get('date')

        if Warehouse.objects.filter(name=name).exists():
            messages.error(request, "A warehouse with this name already exists.")
            return redirect('add_warehouse')
        
        warehouse = Warehouse.objects.create(
            name=name,
            location=location,
            total_capacity=total_capacity,
            available_capacity=available_capacity,
            contact_person_name=contact_person_name,
            contact_person_email=contact_person_email,
            contact_person_phone=contact_person_phone,
            status=status,
            date=date
        )
        warehouse.save
        messages.success(request, "Warehouse added successfully.")
        return redirect('warehouse_view')
    else:
        return HttpResponse("Method Not Allowed", status=405)

def edit_warehouse(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.name = request.POST.get('name')
        warehouse.location = request.POST.get('location')
        warehouse.total_capacity = request.POST.get('total_capacity')
        warehouse.available_capacity = request.POST.get('available_capacity')
        warehouse.contact_person_name = request.POST.get('contact_person_name')
        warehouse.contact_person_email = request.POST.get('contact_person_email')
        warehouse.contact_person_phone = request.POST.get('contact_person_phone')
        warehouse.status = request.POST.get('status')
        warehouse.date = request.POST.get('date')
        warehouse.save()
        return redirect('warehouse_view')
    return HttpResponse("Method Not Allowed", status=405)

def delete_warehouse(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('warehouse_view')
    return HttpResponse("Method Not Allowed", status=405)

def search_warehouse(request):
    search_text = request.GET.get('search_text')
    warehouses = Warehouse.objects.filter(Q(name__icontains=search_text))
    return render(request, 'warehouse/warehouse_views.html', {'warehouses': warehouses})


def storage_type(request):
    storage_types = WarehouseType.objects.all()
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse/storage_type.html', {'storage_types': storage_types, 'warehouses': warehouses})

def add_storage_type(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        rate = request.POST.get('rate')
        capacity = request.POST.get('capacity')
        count = request.POST.get('count')
        warehouse_id = request.POST.get('warehouse_id')  # Get the warehouse_id from the form

        # Check if all required fields are provided
        if type and rate and capacity and count and warehouse_id:
            # Create a new WarehouseType object with the provided data
            WarehouseType.objects.create(
                type=type,
                rate=rate,
                capacity=capacity,
                count=count,
                warehouse_id=warehouse_id  # Set the warehouse_id
            )
            # Redirect to a success URL or render a success message
            return redirect('storage_type')  # Replace 'storage_type' with the appropriate URL name
        else:
            # Handle the case where required fields are missing
            return render(request, 'warehouse/error.html', {'message': 'Missing required fields'})

    # Fetch all warehouses to pass to the template
    warehouses = Warehouse.objects.all()
    
    return render(request, 'warehouse/storage_type.html', {'warehouses': warehouses})


def edit_storage_type(request, storage_type_id):
    storage_type = get_object_or_404(WarehouseType, pk=storage_type_id)
    if request.method == 'POST':
        storage_type.type = request.POST.get('type')
        storage_type.rate = request.POST.get('rate')
        storage_type.capacity = request.POST.get('capacity')
        storage_type.count = request.POST.get('count')
        warehouse_id = request.POST.get('warehouse_id')  # Get the selected warehouse ID
        storage_type.warehouse_id = warehouse_id  # Update the warehouse ID for the storage type
        storage_type.save()
        return redirect('storage_type')  # Redirect back to the storage type page after editing

def delete_storage_type(request, storage_type_id):
    if request.method == 'POST':
        storage_type = WarehouseType.objects.get(pk=storage_type_id)
        storage_type.delete()
        return redirect('storage_type')


def togle_view(request):
    return render(request, 'warehouse/error.html')

def warehouse_template_page(request):
    return render(request, 'base1.html')


from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json


from django.http import HttpResponseBadRequest

from django.shortcuts import render, redirect, HttpResponse
from .models import WarehouseType
import json

def warehouse_booking_page(request):
    if request.method == 'POST':
        selected_seats_json = request.POST.get('data_list')
        selected_seats = json.loads(selected_seats_json)
        warehouse_type_id = request.POST.get('warehouse_type')

        # Check if warehouse_type_id is empty or not a valid integer
        if not warehouse_type_id:
            return HttpResponseBadRequest("Warehouse type ID is empty")
        
        try:
            # Try converting warehouse_type_id to an integer
            warehouse_type_id = int(warehouse_type_id)
        except ValueError:
            return HttpResponseBadRequest("Invalid warehouse type ID")

        try:
            # Retrieve the warehouse type object
            warehouse_type = WarehouseType.objects.get(id=warehouse_type_id)
        except WarehouseType.DoesNotExist:
            return HttpResponseBadRequest("Warehouse type ID does not exist")

        selected_seats_display = ', '.join(selected_seats)  # Join selected seats into a string
        request.session['selected_seats_display'] = selected_seats_display
        request.session['seat'] = selected_seats_display

        # Retrieve warehouse object using warehouse type
        warehouse = warehouse_type.warehouse

        # Save warehouse ID in session
        request.session['warehouse_id'] = warehouse.id

        # Save selected seat numbers and display value to the database
        for seat_number in selected_seats:
            storage_map = StorageMapDup(
                warehouse=warehouse,
                warehouse_type=warehouse_type,
                selected_seats_display=selected_seats_display
            )
            storage_map.save()

        # Redirect to storage_user_details.html
        return redirect('storage_user_details')

    # If the request method is not POST, render the warehouse booking page
    warehouse_type = WarehouseType.objects.first()  # You might need to adjust this query based on your application logic
    return render(request, 'booking/warehouse_booking.html', {'warehouse_type': warehouse_type})

    

import datetime
import uuid
def storage_user_details(request):
    if request.method == 'POST':
        # Generate a unique user ID

        # Retrieve form data
        user=request.user
        warehouse_id = request.POST.get('warehouse')
        warehouse_type_id = request.POST.get('warehouse_type')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        rate = request.POST.get('rate')

        # Save form data to StorageUserDup model
        users = StorageUserDup.objects.create(        
            user=user,       
            warehouse_id=warehouse_id,
            warehouse_type_id=warehouse_type_id,
            productname=product_name,
            quantity=quantity,
            start_date=start_date,
            end_date=end_date,
            total_amount=rate
        )
        users.save()
        request.session['storage_user_instance_id'] = users.id
        # user.user_id
        # Redirect to the payment page
        return redirect('payment_page')  # Replace 'payment_page' with the URL name of your payment page
        
        
    # return render(request, 'booking/storage_user_details.html', {'warehouses': Warehouse.objects.all, 'warehouse_types': WarehouseType.objects.all()})
    return render(request, 'booking/storage_user_details.html', {'warehouses': Warehouse.objects.filter(name="war1"), 'warehouse_types': WarehouseType.objects.all()})




from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


from .models import StorageUserDup
@login_required  # Add the login_required decorator to restrict access to authenticated users only
def  payment_page(request):
    #last_stored_user = StorageUserDup.objects.first()
    last_stored_user = StorageUserDup.objects.filter(is_paid='1').first()
    amount = int(last_stored_user.total_amount) * 100
    currency = 'INR'
    amount = amount  
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['storage_user'] = last_stored_user
    return render(request, 'booking/payment.html', context=context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import StorageUserDup

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Payment, StorageUserDup

@csrf_exempt
def paymenthandler(request):
    storage_user_instance_id = request.session.get('storage_user_instance_id')
    
    # Retrieve the StorageUserDup instance
    storage_user_instance = get_object_or_404(StorageUserDup, id=storage_user_instance_id)
    
    # Create a Payment instance and assign values
    payment_instance = Payment(
        user=storage_user_instance.user,
        warehouse=storage_user_instance.warehouse,
        warehouse_type=storage_user_instance.warehouse_type,
        storage_user=storage_user_instance,
        product_name=storage_user_instance.productname,
        quantity=storage_user_instance.quantity,
        start_date=storage_user_instance.start_date,
        end_date=storage_user_instance.end_date,
        total_amount=storage_user_instance.total_amount,
        is_paid=True,  # Set is_paid to True
        selected_seats_display=request.session.get('selected_seats_display')
    )

    # Save the Payment instance
    payment_instance.save()

    # Delete the StorageUserDup instance
    # storage_user_instance.delete()

    # Render the payment details template and pass payment_instance
    return render(request, 'booking/payment_pdf_template.html', {'payment_instance': payment_instance})

def generate_pdf(request):
    # Retrieve payment instance
    payment_instance = Payment.objects.first()

    # Render the payment details template with payment instance
    template_path = 'booking/payment_pdf_template.html'
    context = {'payment_instance': payment_instance}
    template = get_template(template_path)
    html = template.render(context)

    # Include the success message in the HTML content
    success_message = "Payment processed successfully completed."
    html += f"<p>{success_message}</p>"

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="payment_details.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response