from django.db import models
from django.contrib.auth.models import AbstractUser

# ユーザーモデル
class User(AbstractUser):
    email = models.EmailField(unique=True)  # ユニークなメールアドレス
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    switchbot_token = models.CharField(max_length=255, blank=True, null=True)  # Switchbot APIトークン

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # ここで関連名を変更
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # ここで関連名を変更
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def __str__(self):
        return self.username  # 管理画面などでの表示用

# デバイスモデル
class Device(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # Switchbot APIから取得したデバイスID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーとの関連
    name = models.CharField(max_length=255)  # デバイス名
    type = models.CharField(max_length=255)  # デバイスタイプ（例: カーテン、ボット、ハブなど）
    status = models.CharField(max_length=255)  # デバイスの状態（オン/オフ、バッテリー残量など）
    last_updated = models.DateTimeField(auto_now=True)  # 最終更新日時

    def __str__(self):
        return f"{self.name} ({self.type})"  # デバイス名とタイプを返す

# ログモデル
class Log(models.Model):
    id = models.AutoField(primary_key=True)  # ログID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 操作を行ったユーザー
    device = models.ForeignKey(Device, on_delete=models.CASCADE)  # 操作対象デバイス
    action = models.CharField(max_length=255)  # 実行されたアクション（例: オン/オフ、設定変更）
    timestamp = models.DateTimeField(auto_now_add=True)  # 実行日時

    def __str__(self):
        return f"{self.user.username} - {self.device.name} - {self.action}"  # ログの内容を表示