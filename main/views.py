from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import WeekDay, User, Order, Lunch
from .forms import UserForm, UserLoginForm


def home(request):
    return render(request, "monthly_lunches.html", {})

def lunches(request):
    weekdays = WeekDay.objects.prefetch_related("lunch").all()
    monday = weekdays.get(weekday="Monday")
    tuesday = weekdays.get(weekday="Tuesday")
    wednesday = weekdays.get(weekday="Wednesday")
    thursday = weekdays.get(weekday="Thursday")
    friday = weekdays.get(weekday="Friday")

    return render(request, "lunches.html", {
        "monday": monday,
        "tuesday": tuesday,
        "wednesday": wednesday,
        "thursday": thursday,
        "friday": friday,
    })

def authenticateUser(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Info')

    return render(request, "register.html", {
        "form": form
    })


def loginUser(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        if form.is_valid():
            if User.objects.filter(email__exact=email).exists():
                user = authenticate(email=email, password=password)
                if user != None:
                    login(request, user)
                    return redirect("main:home")
                else:
                    messages.error(request, 'Invalid Password')
            else:
                messages.error(request, 'No user with these credentials')
        else:
            messages.error(request, "Invalid Data")
    return render(request, "login.html", {
        "form": form,
    })

def logoutUser(request):
    logout(request)
    return redirect("/")


def add_launch(request, weekday_id, lunch_id):
    weekday = WeekDay.objects.get(id=weekday_id)
    lunch = Lunch.objects.get(id=lunch_id)

    user = request.user
    orders = Order.objects.filter(user=user, weekday=weekday)

    if orders.exists():
        order = orders[0]
        if order.lunch != lunch:
            order.lunch = lunch
            order.save(update_fields=['lunch'])
            print("Updated")
    elif not orders.exists():
        order = Order.objects.create(
            user=user,
            weekday=weekday,
            lunch=lunch,
        )
        order.save()

    return redirect("/orders")


@login_required
def orders(request):
    user = request.user

    orders = Order.objects.filter(user=user).order_by("weekday_id")
    return render(request, "orders.html", {
        "orders": orders,
    })


def rules(request):
    return render(request, "rules.html")


@login_required
def balance(request):
    balance = request.user.balance
    return render(request, "balance.html",  {
        "balance": balance,
    })

@login_required
def payment(request):
    user = request.user
    orders = Order.objects.filter(user=user, paid=False)

    sum = 0
    for order in orders:
        sum += order.get_total

    return render(request, "payment.html", {
        "orders": orders,
        "sum": sum,
    })


def remove_order(request, weekday_id, lunch_id):
    user = request.user
    order = Order.objects.get(user=user, weekday_id=weekday_id, lunch_id=lunch_id)
    order.delete()
    return redirect("/orders")


def pay(request):
    user = request.user
    orders = Order.objects.filter(user=user, paid=False)

    sum = 0
    for order in orders:
        sum += order.get_total

    if user.balance < sum:
        messages.error(request, 'Not enough money')
        return render(request, "payment.html")
    else:
        user.balance -= sum
        for order in orders:
            order.paid = True
            order.save(update_fields=['paid'])

        user.save(update_fields=['balance'])


    return redirect("/orders")

