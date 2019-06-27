from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Thanks {username}. Please confirm your email.")
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})
