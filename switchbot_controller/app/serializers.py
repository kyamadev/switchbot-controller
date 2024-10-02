from rest_framework import serializers
from .models import User, Device, Log

# Userシリアライザー
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin','switchbot_token']  # 必要なフィールドを指定

# Deviceシリアライザー
class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # デバイスの所有者（ユーザー）の情報をネストする

    class Meta:
        model = Device
        fields = ['id', 'name', 'type', 'status', 'last_updated', 'user']  # 必要なフィールドを指定

# Logシリアライザー
class LogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # ログに関連するユーザー情報
    device = DeviceSerializer(read_only=True)  # ログに関連するデバイス情報

    class Meta:
        model = Log
        fields = ['id', 'user', 'device', 'action', 'timestamp']  # 必要なフィールドを指定