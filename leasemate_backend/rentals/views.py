from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import RentListing
from .serializers import RentListingSerializer
from leasemate_authentication.serializers import ProfileSerializer  # Assuming you have this serializer for user

class RentListingCreateView(APIView):
    """
    View for adding a new rent listing.
    """
    serializer_class = RentListingSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to create a new rent listing.
        """
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        print(f"Request headers: {request.headers}")  # Debugging line
        serializer = RentListingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate listing with logged-in user
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RentListView(APIView):
    """
    View to retrieve all rent listings.
    """
    serializer_class = RentListingSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to retrieve all rent listings.
        """
        try:
            rent_listings = RentListing.objects.select_related('user').all()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = []
        for rent_listing in rent_listings:
            rent_listing_data = RentListingSerializer(rent_listing, context={'request': request}).data
            response_data.append(rent_listing_data)

        return Response(response_data, status=status.HTTP_200_OK)


class ChatWithOwnerView(APIView):
    """
    View to retrieve the full user profile of the owner of a rent listing.
    """
    permission_classes = [AllowAny]

    def get(self, request, rent_listing_id):
        try:
            rent_listing = RentListing.objects.select_related('user').get(pk=rent_listing_id)
        except RentListing.DoesNotExist:
            return Response({"error": "Rent listing not found."}, status=status.HTTP_404_NOT_FOUND)

        owner = rent_listing.user
        user_data = ProfileSerializer(owner).data  # Return full user profile

        return Response({
            "owner_profile": user_data
        }, status=status.HTTP_200_OK)
