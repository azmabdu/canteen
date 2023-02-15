from django.contrib import admin
from .models import User, Lunch, MenuItem, Order, WeekDay, Category

admin.site.register(User)
admin.site.register(Lunch)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(WeekDay)
admin.site.register(Category)
