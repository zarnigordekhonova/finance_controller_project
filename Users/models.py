from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='Profile_pictures/Users', blank=True, null=True, default='Profile_pictures/default_picture.png')
    phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'custom_user'


    def __str__(self):
        return f"{self.username} - {self.email}"
