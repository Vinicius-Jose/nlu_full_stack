from django.db import models


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
CAR_TYPES = [
    ("SEDAN", "SEDAN"),
    ("SUV", "SUV"),
    ("WAGON", "WAGON"),
]


class CarMake(models.Model):
    name = models.CharField(max_length=100, blank=False, default="")
    description = models.TextField(max_length=100)

    def __str__(self) -> str:
        return f"Name: {self.name} Description: {self.description}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    car_type = models.CharField(choices=CAR_TYPES, max_length=100)
    year = models.DateField()

    def __str__(self) -> str:
        return (
            f"Car Make:{self.car_make} Name: {self.name} "
            + f"DealerId: {self.dealer_id} Type: {self.car_type} Year {self.year}"
        )


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(
        self, address, city, full_name, id, lat, long, short_name, st, zip_code
    ):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip_code = zip_code

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(
        self,
        dealership,
        name,
        purchase,
        review,
        purchase_date,
        car_make,
        car_model,
        car_year,
        id,
    ) -> None:
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = None
        self.id = id
