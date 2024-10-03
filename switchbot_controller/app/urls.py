from django.urls import path
from .views import device_list, device_status, control_device_view, log_list, update_switchbot_token, login_view, signup_view

urlpatterns = [
    path('devices/', device_list, name='device-list'),
    path('devices/<str:device_id>/status/', device_status, name='device-status'),
    path('devices/<str:device_id>/control/', control_device_view, name='device-control'),
    path('logs/', log_list, name='log-list'),
    path('update-token/', update_switchbot_token, name='update-switchbot-token'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]