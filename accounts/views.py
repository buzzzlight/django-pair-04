from django.shortcuts import redirect, render
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.decorators import login_required


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("reviews:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("reviews:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("reviews:index")


def detail(request, pk):
    account_detail = User.objects.get(pk=pk)
    context = {"account_detail": account_detail}
    return render(request, "accounts/detail.html", context)


@login_required

def update(request, pk):
    if request.user.pk == pk:
        if request.method == "POST":
            update_form = CustomUserChangeForm(request.POST, instance=request.user)
            if update_form.is_valid():
                update_form.save()
                return redirect("accounts:detail", request.user.pk)
        else:
            update_form = CustomUserChangeForm(instance=request.user)
        context = {"update_form": update_form}
        return render(request, "accounts/update.html", context)
    else:
        return render(request, 'reviews/index.html')

