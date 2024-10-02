from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, Log
from .serializers import DeviceSerializer, LogSerializer, UserSerializer
from .switchbot import get_device_list, get_device_status, control_device

# デバイス一覧取得エンドポイント
@api_view(['GET'])
def device_list(request):
    devices = get_device_list(request.user)  # ユーザーごとのトークンを使う
    if devices is not None:
        return Response(devices)
    return Response({"error": "Failed to fetch devices or token missing"}, status=500)

# デバイスステータス取得エンドポイント
@api_view(['GET'])
def device_status(request, device_id):
    status = get_device_status(request.user, device_id)
    if status is not None:
        return Response(status)
    return Response({"error": "Failed to fetch device status or token missing"}, status=500)

# デバイス操作エンドポイント
@api_view(['POST'])
def control_device_view(request, device_id):
    command = request.data.get("command")
    result = control_device(request.user, device_id, command)
    if result is not None:
        return Response(result)
    return Response({"error": "Failed to control device or token missing"}, status=500)

# 操作ログ取得エンドポイント
@api_view(['GET'])
def log_list(request):
    logs = Log.objects.filter(user=request.user)
    serializer = LogSerializer(logs, many=True)
    return Response(serializer.data)

# Switchbotトークンの登録・更新エンドポイント
@api_view(['POST'])
def update_switchbot_token(request):
    user = request.user
    token = request.data.get('switchbot_token')

    if token:
        user.switchbot_token = token
        user.save()
        return Response({"message": "Switchbot token updated successfully"}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)