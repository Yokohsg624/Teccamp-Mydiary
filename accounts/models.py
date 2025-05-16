from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 一般ユーザーおよびスーパーユーザーを作成するクラス
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password,
            is_active=True
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    
# 修正後の CustomUser モデル
class CustomUser(AbstractBaseUser):
    username = models.CharField(
        'ユーザー名',
        max_length=20,
        unique=True,
        error_messages={'unique': ("同一のユーザー名が既に登録されています")}
    )
    email = models.EmailField('メールアドレス', unique=True)
    is_staff = models.BooleanField(default=False)  # 管理画面にアクセスできるか
    is_superuser = models.BooleanField(default=False)  # 全権限を持つか
    is_active = models.BooleanField(default=True)  # ユーザーが有効か
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        # 任意の権限があるか（全権限を持つユーザーは常に True）
        return True

    def has_module_perms(self, app_label):
        # アプリケーションにアクセスできるか（全権限を持つユーザーは常に True）
        return True
    
    