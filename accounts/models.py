from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, PermissionsMixin
from django.core.validators import RegexValidator


# Create your models here.

class User(User, PermissionsMixin):

    _meta = None

    def __str__(self):
        return self.username


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='addresses', on_delete=models.CASCADE)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    district = models.ForeignKey("District", on_delete=models.CASCADE)
    ward = models.ForeignKey("Ward", on_delete=models.CASCADE, blank=True, null=True)
    home = models.CharField(max_length=255, blank=False, null=False)
    full_name = models.CharField(max_length=255, blank=False, null=False, default="")
    phone = models.CharField(validators=[
        RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Số điện thoại phải đúng định dạng '0123 456 789'."), ],
                             max_length=10, blank=False, null=False, default="")

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.home} - phường/xã {self.ward}," \
               f" {self.district}, {self.city}"

    class Meta:
        verbose_name_plural = 'Addresses'


class City(models.Model):
    objects = None
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'


class District(models.Model):
    city = models.ForeignKey(City, related_name='districts', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f" {self.name}" if self.name.split()[0] != 'Quận' else self.name


class Ward(models.Model):
    district = models.ForeignKey(District, related_name='wards', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
