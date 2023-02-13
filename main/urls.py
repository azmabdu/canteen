from django.urls import path, include
from .views import *


app_name = "main"

urlpatterns = [
    path('lunches', lunches, name="lunches"),
    path('register', authenticateUser, name="register"),
    path('login', loginUser, name="login"),
    path('logout', logoutUser, name="logout"),
    path('rules', rules, name="rules"),
    path('balance', balance, name="balance"),
    path('payment', payment, name="payment"),
    path('orders', orders, name="orders"),
    path('', home, name="home"),

    path('pay', pay, name="pay"),
    path('remove-order/<int:weekday_id>/<int:lunch_id>', remove_order, name="remove-order"),
    path('add-launch/<int:weekday_id>/<int:lunch_id>', add_launch, name="add-launch"),
]