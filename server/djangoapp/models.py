from django.db import models
from django.utils.timezone import now


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


# <HINT> Create a plain Python class `DealerReview` to hold review data
