import requests
from django.conf import settings

BASE_URL = "https://api.switch-bot.com/v1.1"

# デバイス一覧を取得する関数
def get_device_list(user):
    token = user.switchbot_token  # ユーザーごとのトークンを取得
    if not token:
        return None  # トークンが存在しない場合
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}/devices"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# デバイスの状態を取得する関数
def get_device_status(user, device_id):
    token = user.switchbot_token
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}/devices/{device_id}/status"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# デバイスを操作する関数
def control_device(user, device_id, command):
    token = user.switchbot_token
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}/devices/{device_id}/commands"
    data = {
        "command": command,
        "parameter": "default",
        "commandType": "command"
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None