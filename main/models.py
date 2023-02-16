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
    weekday = models.CharField(max_length=255, choices=WEEK_DAYS, unique=True)
    lunch = models.ManyToManyField(Lunch, related_name="weekday", blank=True)

    def __str__(self):
        return f"{self.weekday}"

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=255, blank=False, null=False)
    balance = models.DecimalField(max_digits=1000, default=1_000_000, blank=True, decimal_places=2)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="menuitems")
    lunch = models.ManyToManyField(Lunch, blank=True, related_name="menuitem")
    title = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=1000, decimal_places=2,)

    def __str__(self):
        return f"{self.title}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    weekday = models.ForeignKey(WeekDay, on_delete=models.CASCADE, related_name="orders")
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE, related_name="lunch")
    paid = models.BooleanField(default=False)

    @property
    def get_total (self):
        return self.lunch.total_price

    class Meta:
        unique_together = ('user', 'lunch', 'weekday')

    def __str__(self):
        return f"{self.user}: {self.lunch}"
