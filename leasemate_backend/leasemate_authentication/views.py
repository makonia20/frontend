import logging
from rest_framework.permissions import AllowAny
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, get_user_model
from .serializers import SignupSerializer, LoginSerializer, ProfileSerializer

LeasemateUser = get_user_model()

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        # Override to disable CSRF check
        return

@method_decorator(csrf_exempt, name='dispatch')
class ProfileAPIView(APIView):
    """Profile API View"""
    permission_classes = [AllowAny]

    def get(self, request):
        logger.info(f"Request received: {request.method} {request.path}")

        username = request.query_params.get('username')
        if username:
            try:
                user = LeasemateUser.objects.get(username=username)
            except LeasemateUser.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=404)
        else:
            # Allow unauthenticated access by returning user info with "N/a" placeholders
            if not request.user.is_authenticated:
                na_data = {
                    'username': 'N/a',
                    'phone': 'N/a',
                    'id_number': 'N/a',
                    'first_name': 'N/a',
                    'middle_name': 'N/a',
                    'last_name': 'N/a',
                    'session_id': None
                }
                return Response(na_data, status=200)
            user = request.user

        serializer = ProfileSerializer(user)
        session_id = request.session.session_key  # Get the session ID
        response_data = serializer.data
        response_data['session_id'] = session_id  # Include session ID in the response
        return Response(response_data)  # Return the response with session ID

@method_decorator(csrf_exempt, name='dispatch')
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)  # Use updated SignupSerializer
        if serializer.is_valid():
            user = serializer.save()  # Create the user
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)  # Use updated LoginSerializer
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Log the user in and create a session
            request.session.save()  # Ensure session is saved
            session_id = request.session.session_key  # Get the session ID
            return Response({
                'message': 'Login successful',
                'redirect_url': '/auth/profile/',  # Provide the redirect URL
                'session_id': session_id  # Include session ID in response
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
