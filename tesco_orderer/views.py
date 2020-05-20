from django.shortcuts import render, redirect, Http404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from CustomUser.models import User
from orders.models import Order
from django.db.utils import IntegrityError
from django.conf import settings
from cryptography.fernet import Fernet


def home(r):
    orders = Order.objects.filter(creator=r.user.id)
    return render(r, "home.html", {"orders": orders})


def add_slot(r):
    if r.method != "POST":
        raise Http404

    min_date = r.POST["min-date"]
    max_date = r.POST["max-date"]
    min_time = r.POST["min-time"]
    max_time = r.POST["max-time"]

    order = Order(min_date=min_date, max_date=max_date, min_time=min_time, max_time=max_time, creator=r.user)
    order.save()

    return redirect("/")


def view_login(r):
    if r.method == "GET":
        if not r.user.is_authenticated:
            return render(r, "login.html")
        else:
            return redirect("/")
    elif r.method == "POST":
        firstname = r.POST["firstname"]
        password = r.POST["password"]
        user = authenticate(r, username=firstname, password=password)
        if user is not None:
            login(r, user)
            next_page = r.GET.get("next")
            if next_page:
                return redirect(next_page)
            return redirect("/")
        return render(r, "login.html", {"error": "Incorrect Login"})
    else:
        raise Http404


def view_signup(r):
    if not r.user.is_authenticated:
        if r.method == "GET":
            return render(r, "signup.html")
        elif r.method == "POST":
            ref = r.POST["ref"]
            if ref.lower() != settings.REFERRAL:
                return render(r, "signup.html", {"error": "Incorrect Key"})
            username = r.POST["firstname"]
            email = r.POST["email"]
            password = r.POST["password"]
            key = Fernet(settings.TESCO_PASSWORD_ENCRYPTION)
            tesco_password = key.encrypt(r.POST["tesco-password"].encode("utf-8")).decode("utf-8")
            if username and email and password and tesco_password:
                try:
                    User.objects.create_user(username=username, email=email, password=password, tesco_password=tesco_password)
                    next_page = r.GET.get("next")
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect("/")
                except IntegrityError:
                    return render(r, "signup.html", {"error": "Name already used."})
            else:
                return render(r, "signup.html", {"error": "Please fill in all of the boxes."})
        else:
            raise Http404
    else:
        return redirect("/")


def view_logout(r):
    logout(r)
    return redirect("/")


def change_account(r):
    if r.method == "GET":
        return render(r, "change_account.html")
    elif r.method == "POST":
        if r.POST.get("newpassword"):
            r.user.set_password(r.POST["newpassword"])
            r.user.save()
            return render(r, "change_account.html")
        else:
            if r.user.check_password(r.POST.get("password")):
                new_name = r.POST.get("firstname")
                new_email = r.POST.get("email")
                new_tesco_pass = r.POST.get("tesco-password")
                if new_name:
                    r.user.username = new_name
                if new_email:
                    r.user.email = new_email
                if new_tesco_pass:
                    key = Fernet(settings.TESCO_PASSWORD_ENCRYPTION)
                    new_tesco_pass = key.encrypt(new_tesco_pass.encode("utf-8")).decode("utf-8")
                    r.user.tesco_password = new_tesco_pass
                r.user.save()
                return render(r, "change_account.html")
            else:
                return render(r, "change_account.html", {"error": "Incorrect password. You can reset it below."})
    else:
        raise Http404


def remove_order(r, order):
    order_object = Order.objects.get(id=order)
    if order_object.creator_id == r.user.id:
        order_object.delete()
        return JsonResponse({"success": "y"})
    else:
        return JsonResponse({"success": "n"})
