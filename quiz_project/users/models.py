from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=60)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = BaseUserManager()

    class Meta:
        db_table = 'tbl_users'

    @staticmethod
    def create(username, password, email):
        user = CustomUser(username=username, email=email)
        user.set_password(password)
        try:
            user.save()
            return user
        except IntegrityError:
            return None

    @staticmethod
    def get_by_username(username):
        try:
            return CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return None