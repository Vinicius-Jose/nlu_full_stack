import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime

import json

from djangoapp.restapis import get_dealers_from_cf
from djangoapp.restapis import get_dealer_reviews_from_cf
from djangoapp.restapis import post_request

from dotenv import load_dotenv
import os

from djangoapp.models import CarModel

load_dotenv()

# Get an instance of a logger
logger = logging.getLogger(__name__)

REVIEW_URL = os.getenv("REVIEW_URL")
DEALERSHIP_URL = os.getenv("DEALERSHIP_URL")

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html", {})


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html", {})


# Create a `login_request` view to handle sign in request
def login_request(request):
    # Get username and password from request.POST dictionary
    username = request.POST["user_name"]
    password = request.POST["pwd"]
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
    return redirect("djangoapp:index")


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    user_exist = False
    username = request.POST.get("user_name")
    password = request.POST.get("pwd")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    try:
        # Check if user already exists
        User.objects.get(username=username)
        user_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug(f"{username} is new user")
    # If it is a new user
    if not user_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
    return redirect("djangoapp:index")


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = DEALERSHIP_URL
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Return a list of dealer short name
        context["dealerships"] = dealerships
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = REVIEW_URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        return render(request, "djangoapp/dealer_details.html", context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    context = {}
    if not User.is_authenticated:
        return redirect("djangoapp:registration")
    elif request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        dealer = get_dealers_from_cf(DEALERSHIP_URL, dealerId=dealer_id)
        context["dealer_id"] = dealer_id
        context["cars"] = cars
        context["dealer"] = dealer[0]
        return render(request, "djangoapp/add_review.html", context)
    selected_car = request.POST.get("car")
    selected_car: CarModel = CarModel.objects.get(id=selected_car)

    review = {
        "time": datetime.utcnow().isoformat(),
        "dealership": dealer_id,
        "review": request.POST.get("review"),
        "car_make": selected_car.car_make.name,
        "car_model": selected_car.car_type,
        "car_year": selected_car.year.strftime("%Y"),
        "name": selected_car.name,
        "purchase": request.POST.get("purchasecheck"),
        "purchase_date": request.POST.get("purchasedate"),
    }

    json_payload = {"review": review}
    print(json_payload)
    result = post_request(url=REVIEW_URL, review=review, dealerId=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
