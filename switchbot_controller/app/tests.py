from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch  # 追加
from .models import Device

class APITestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.device = Device.objects.create(id='testdevice', user=self.user, name='Test Device', type='Bot')

    @patch('app.views.get_device_list')  # モックの追加
    def test_device_list(self, mock_get_device_list):
        # モックのレスポンスを定義
        mock_get_device_list.return_value = [{'id': 'testdevice', 'name': 'Test Device', 'status': 'on'}]
        
        # APIリクエスト
        url = reverse('device-list')
        response = self.client.get(url)
        
        # 期待されるレスポンスを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'id': 'testdevice', 'name': 'Test Device', 'status': 'on'}])

    @patch('app.views.get_device_status')  # モックの追加
    def test_device_status(self, mock_get_device_status):
        # モックのレスポンスを定義
        mock_get_device_status.return_value = {'status': 'on'}
        
        # APIリクエスト
        url = reverse('device-status', args=[self.device.id])
        response = self.client.get(url)
        
        # 期待されるレスポンスを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'on'})

    @patch('app.views.control_device')  # モックの追加
    def test_device_control(self, mock_control_device):
        # モックのレスポンスを定義
        mock_control_device.return_value = {'result': 'success'}
        
        # APIリクエスト
        url = reverse('device-control', args=[self.device.id])
        response = self.client.post(url, {'command': 'turnOn'}, format='json')
        
        # 期待されるレスポンスを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'result': 'success'})