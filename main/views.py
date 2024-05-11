from rest_framework import status
from rest_framework.views import APIView
from main.serializers import ResgisterSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import MyUser 
import jwt, datetime
# Create your views here.
#Register
class RegisterView(APIView):
    serializer_class = ResgisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        extra_fields = {k: v for k, v in validated_data.items() if k not in ('username', 'email', 'password')}

        # Using the custom create_user method
        MyUser.objects.create_user(username, email, password, **extra_fields)

        response_data = {
            'message': f"Successfully created a new user {username}",
            'status': 201
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    def post(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        # Determine if the user is logging in with username or email
        if '@' in username_or_email:
            # Assume it's an email address
            try:
                user = MyUser.objects.get(email=username_or_email)
                username = user.username
            except MyUser.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # It's a username
            username = username_or_email

        user = authenticate(username=username, password=password)
        if user is not None:
            # Successful login
            # Here you can include code to create and return a token if needed
            payload = {
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat' : datetime.datetime.utcnow()

            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response = Response()
            response.set_cookie(key = 'jwt', value = token, httponly=True)
            response.data = {
                'jwt' : token
            }
            return response
        else:
            # Authentication failed
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"})
        # Clear the JWT cookie by setting its expiration to the past
        response.delete_cookie('jwt')
        return response
