"""
This module contains all the database models for our project.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create User Manager object
class UserManager(BaseUserManager):
    """Manager for users."""

    # The **extra_fields is added so that if the developer added extra fields
    # in the future, it will be handled properly.
    def create_user(self, email, password='None', **extra_fields):
        """Create, save and return a new user."""
        # ValueError is built-in in Django so no need to import it.
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # handles saving the user to a db or multiple db's
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Assign this particular user to our User Manager.
    # The syntax is Django-specific.
    objects = UserManager()
    # Field that we want to use for authentication
    USERNAME_FIELD = 'email'
