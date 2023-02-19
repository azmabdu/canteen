from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager


WEEK_DAYS = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
)

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

class Lunch(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    @property
    def total_price(self):
        sum = 0
        for item in self.menuitem.all():
            sum += item.price
        return sum

    def __str__(self):
        return f"{self.name}"


class WeekDay(models.Model):
    weekday = models.CharField(max_length=255, choices=WEEK_DAYS)
    datetime = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.weekday} - {self.datetime}"



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=255, blank=False, null=False)
    balance = models.DecimalField(max_digits=1000, default=1_000_000, blank=True, decimal_places=2)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()



class MenuItem(models.Model):
    lunch = models.ForeignKey(Lunch, on_delete=models.PROTECT, related_name="menuitem")
    date = models.ForeignKey(WeekDay, on_delete=models.PROTECT, related_name="menuitems")
    title = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=1000, decimal_places=2, default=10000.00)

    def __str__(self):
        return f"{self.title} - {self.lunch}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    weekday = models.ForeignKey(WeekDay, on_delete=models.CASCADE, related_name="orders")
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    paid = models.BooleanField(default=False)

    @property
    def get_total (self):
        return self.menuitem.price

    class Meta:
        unique_together = ('user', 'menuitem', 'weekday')

    def __str__(self):
        return f"{self.user}: {self.menuitem}"
