import requests
import json

# import related models here
from requests.auth import HTTPBasicAuth

from djangoapp.models import CarDealer
from djangoapp.models import DealerReview
from dotenv import load_dotenv
import os

load_dotenv()
WATSON_URL = os.getenv("WATSON_URL")
WATSON_API_KEY = os.getenv("WATSON_API_KEY")


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs) -> dict:
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get("api_key")
    if api_key:
        kwargs.pop("api_key")
    try:
        auth = HTTPBasicAuth("apikey", api_key)
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={"Content-Type": "application/json"},
            params=kwargs,
            auth=auth if api_key else None,
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response.json()


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, **kwargs) -> dict:
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get("api_key")
    if api_key:
        kwargs.pop("api_key")
    try:
        auth = HTTPBasicAuth("apikey", api_key)
        # Call get method of requests library with URL and parameters
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=kwargs,
            auth=auth if api_key else None,
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response.json()


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs) -> list[CarDealer]:
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        # For each dealer object
        for dealer in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip_code=dealer["zip"],
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs) -> list[DealerReview]:
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as reviewrs
        # For each review object
        for review in json_result:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                id=review.get("id", review.get("_id", 0)),
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    url = WATSON_URL
    params = dict()
    params["text"] = dealer_review
    params["version"] = "2019-07-12"
    params["language"] = "en"
    params["api_key"] = WATSON_API_KEY
    params["features"] = {
        "sentiment": {},
        "categories": {},
        "concepts": {},
        "entities": {},
        "keywords": {},
        "emotion": {},
    }
    sentiment = get_request(url, **params)
    emotion: dict = sentiment.get("emotion", {}).get("document", {}).get("emotion", {})
    bigger_emotion = ["sadness", 0]
    for key, value in emotion.items():
        if value > bigger_emotion[1]:
            bigger_emotion[0] = key
            bigger_emotion[1] = value
    sentiment = bigger_emotion[0]
    if sentiment in ("sadness", "disgust", "anger"):
        sentiment = "negative"
    elif sentiment == "joy":
        sentiment = "positive"
    else:
        sentiment = "neutral"
    return sentiment
