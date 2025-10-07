from django.db import models
import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)  # Hash a senha
        user.save(using=self._db)  # Usa o banco de dados correto
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)

class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100, blank=True) 
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Campos obrigatórios para criar um superusuário

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    # Preenche username com a parte local do email contendo apenas letras e garante unicidade.
    def save(self, *args, **kwargs):
        base_username = re.sub(r'[^a-zA-Z]', '', self.email.split('@')[0])
        if not base_username:
            base_username = 'user'

        candidate = base_username
        suffix = 1
        username_qs = MyUser.objects.filter(username=candidate)
        if self.pk:
            username_qs = username_qs.exclude(pk=self.pk)

        while username_qs.exists():
            candidate = f'{base_username}{suffix}'
            suffix += 1
            username_qs = MyUser.objects.filter(username=candidate)
            if self.pk:
                username_qs = username_qs.exclude(pk=self.pk)

        self.username = candidate
        super(MyUser, self).save(*args, **kwargs)
