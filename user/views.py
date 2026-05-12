from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({
        'message': 'Hello, World!'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):

    data = request.data

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not (username and email and password):
        return Response(
            {'message': 'Please enter username, email and password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'message': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'message': 'Email already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'User created successfully.',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    data = request.data

    username = data.get('username')
    password = data.get('password')

    if not (username and password):
        return Response(
            {'message': 'Please enter username and password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(username=username).first()

    if not user:
        return Response(
            {'message': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not user.check_password(password):
        return Response(
            {'message': 'Wrong password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'Login successful.',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['GET'])
def profile(request):

    user = request.user

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })