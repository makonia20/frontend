from rest_framework import serializers
from .models import RentListing, RentImage
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for displaying owner's name and username.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']  # Include username

class RentImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the RentImage model to return image URLs.
    """
    class Meta:
        model = RentImage
        fields = ['id', 'image']

class RentListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the RentListing model, handling image uploads and user info.
    """
    images = serializers.SerializerMethodField()
    owner_first_name = serializers.CharField(source='user.first_name', read_only=True)
    owner_last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = RentListing
        fields = [
            'id', 'user', 'location', 'description', 'country', 'city',
            'roomDetails', 'price', 'houseType', 'numberOfRooms', 'painted', 'ceiling',
            'electricity', 'solar', 'durawalled', 'fenced', 'images', 'created_at',
            'owner_first_name', 'owner_last_name'
        ]
        read_only_fields = ['user']

    def get_images(self, obj):
        """
        Returns serialized image data for the rent listing.
        """
        return RentImageSerializer(obj.images.all(), many=True).data

    def create(self, validated_data):
        """
        Create RentListing with image uploads.
        """
        request = self.context.get('request')
        images_data = request.FILES.getlist('images') if request else []

        # Assign the logged-in user
        validated_data['user'] = request.user
        rent_listing = RentListing.objects.create(**validated_data)

        # Create associated images
        for image_data in images_data:
            RentImage.objects.create(rent_listing=rent_listing, image=image_data)

        return rent_listing
