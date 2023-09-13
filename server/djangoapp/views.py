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

# Get an instance of a logger
logger = logging.getLogger(__name__)


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


# ...


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
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
