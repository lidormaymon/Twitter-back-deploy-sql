from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ..seralizer import CustomUserSerializer
from ..models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        #Adding custom data to token
        token['username'] = user.username
        token['email'] = user.email
        token['staff'] = user.is_staff 
        token['last_login'] = str(user.last_login)
        token['super_user'] = user.is_superuser
        token['is_verified'] = user.is_verified
        token['email'] = user.email
        token['image'] = str(user.profile_image.url) if user.profile_image else None
        token['date_joined'] = str(user.date_joined)
        token['display_name'] = str(user.display_name)
        token['bio'] = str(user.bio)
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    existUser = CustomUser.objects.filter(username = request.data['username'])
    if not existUser:
        if serializer.is_valid():
            email_subject = "Registration Successful"
            email_message = f"Thank you for registering to our website {request.data['username']}."
            from_email = settings.DEFAULT_FROM_EMAIL  # Use your desired sender email
            try:
                send_mail(email_subject, email_message, from_email, [request.data['email']])
            except Exception as e:
                # Handle email sending error, you can log it or return an error response
                print(f"Email sending error: {e}")
                return Response({"error": "Email sending failed"}, status=500)

            if request.data['image'] == '':
                image = 'defaultProfile.jpg'
            else:
                image = request.data['image']

            user = CustomUser.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                display_name=request.data['display_name'],
                profile_image=image
            )

            return Response({"reg": "success"})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)
    else:
        print('409 Error, username already exist')
        return Response('User already exists', status=409)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['message'] = 'Login successful.'
        else:
            response.data['message'] = 'Invalid login credentials.'
        return response

class UserViewSet(APIView):
    def get(self, request, pk=None):
        if pk:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Exclude 'username' field from the request data
        request_data = request.data.copy()
        request_data.pop('username', None)  # Remove 'username' field if present

        serializer = CustomUserSerializer(user, data=request_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Searching user entry point

@api_view(['GET'])
def search_users(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')  # Get the search query from the request

        if not query:
            return ' '
        # Perform a case-insensitive search for usernames
        matching_users = CustomUser.objects.filter(username__icontains=query)
        matching_users = [user for user in matching_users if user.username.lower() != 'admin']

        

        usernames = [user.id for user in matching_users if user.username.startswith(query)]
        return Response({'usernames': usernames})
    
