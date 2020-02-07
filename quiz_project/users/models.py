"""User model"""
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError


class CustomUser(AbstractBaseUser):
    """User model class, extends Base Django User"""
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = BaseUserManager()

    class Meta:
        db_table = 'tbl_users'

    @staticmethod
    def create(username, password, email):
        """
        Creates user instance and tries to add it into database.
        Returns:
            user instance if added successfully,
            None otherwise.
        """
        user = CustomUser(username=username, email=email)
        user.set_password(password)
        try:
            user.save()
            return user
        except IntegrityError:
            return None

    @staticmethod
    def get_by_username(username):
        """
        Returns:
            user instance if found,
            None otherwise.
        """
        try:
            return CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def change_password(username, new_password):
        """
        Method to change user password.
        Returns:
            user instance if password was changed,
            None otherwise.
        """
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        user.set_password(new_password)
        try:
            user.save()
            return user
        except IntegrityError:
            return None
