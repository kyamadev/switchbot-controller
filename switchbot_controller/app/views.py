from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Device, Log
from .serializers import DeviceSerializer, LogSerializer, UserSerializer
from .switchbot import get_device_list, get_device_status, control_device

User = get_user_model()

# デバイス一覧取得エンドポイント
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def device_list(request):
    try:
        devices = get_device_list(request.user)  # ユーザーごとのトークンを使う
        if devices is not None:
            return JsonResponse({'devices': devices}, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Failed to fetch devices or token missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# デバイスステータス取得エンドポイント
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def device_status(request, device_id):
    try:
        status = get_device_status(request.user, device_id)
        if status is not None:
            return JsonResponse(status, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Failed to fetch device status or token missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# デバイス操作エンドポイント
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def control_device_view(request, device_id):
    command = request.data.get('command')
    try:
        result = control_device(request.user, device_id, command)  # SwitchBot API と連携
        return JsonResponse({'status': 'success', 'result': result}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 操作ログ取得エンドポイント
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def log_list(request):
    try:
        logs = Log.objects.filter(user=request.user)
        serializer = LogSerializer(logs, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Switchbotトークンの登録・更新エンドポイント
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_switchbot_token(request):
    token = request.data.get('switchbot_token')
    if token:
        try:
            request.user.switchbot_token = token
            request.user.save()
            return JsonResponse({"message": "Switchbot token updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# ログインエンドポイント
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# サインアップエンドポイント
@api_view(['POST'])
def signup_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)