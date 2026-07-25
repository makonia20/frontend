from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RentListing(models.Model):
    """
    Model for representing a rent listing.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_listings')
    location = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    roomDetails = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    houseType = models.CharField(max_length=50, choices=[
        ('Flat', 'Flat'),
        ('Main House', 'Main House'),
        ('Cottage', 'Cottage'),
        ('Bachelor', 'Bachelor'),
        ('Other', 'Other'),
    ])
    numberOfRooms = models.IntegerField()
    painted = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    ceiling = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    electricity = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    solar = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    durawalled = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    fenced = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.houseType} in {self.location} - {self.city}, {self.country}"

class RentImage(models.Model):
    """
    Model to store images associated with a rent listing.
    """
    rent_listing = models.ForeignKey(RentListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rent_images/')

    def __str__(self):
        return self.image.name
