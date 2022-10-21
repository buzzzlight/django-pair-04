from django.shortcuts import render, redirect
from .forms import MailingForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Mailing

# Create your views here.
@login_required
def index(request):
    mail = Mailing.objects.filter(recipient_id=request.user.id, garbage=False).order_by("-created_at")
    context = {
        "mail": mail,
    }
    return render(request, "mailing/index.html", context)

@login_required
def create(request):
    form = MailingForm(request.POST)
    to_info = get_user_model().objects.get(pk=request.user.id)
    if form.is_valid():
        from_info = get_user_model().objects.get(email=request.POST["to_email"])
        for i in from_info:
            temp = form.save(commit=False)
            temp.recipient_id = i.id
            temp.from_name = to_info.username
            temp.from_email = to_info.email
            temp.save()
        return redirect("mailing:index")
    context = {
        "form": form,
    }
    return render(request, "mailing/create.html", context)


@login_required
def sending(request, pk):
    from_info = get_user_model().objects.get(pk=pk)
    form = MailingForm(request.POST or None, initial={"to_email": from_info.email})
    to_info = get_user_model().objects.get(pk=request.user.id)
    if form.is_valid():
        from_info = get_user_model().objects.filter(email=request.POST["to_email"])
        for i in from_info:
            temp = form.save(commit=False)
            temp.recipient_id = i.id
            temp.from_name = to_info.username
            temp.from_email = to_info.email
            temp.save()
        return redirect("mailing:index")
    context = {
        "form": form,
    }
    return render(request, "mailing/create.html", context)


@login_required
def detail(request, pk):
    mail = Mailing.objects.get(pk=pk)
    if not mail.read:
        mail.read = True
        mail.save()
    context = {
        "mail": mail,
    }
    return render(request, "mailing/detail.html", context)


@login_required
def sent(request):
    mail = Mailing.objects.filter(from_name=request.user).order_by("-created_at")
    context = {
        "mail": mail,
    }
    return render(request, "mailing/sent.html", context)


@login_required
def bin(request):
    bin = Mailing.objects.filter(recipient_id=request.user.id, garbage=True).order_by("-created_at")
    context = {
        "mail": bin,
    }
    return render(request, "mailing/bin.html", context)


@login_required
def important(request):
    important = Mailing.objects.filter(recipient_id=request.user.id, garbage=False, important=True).order_by("-created_at")
    context = {
        "mail": important,
    }
    return render(request, "mailing/important.html", context)


@login_required
def delete(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.delete()
    return redirect("mailing:trash_can")


@login_required
def important_check(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.important = True
    mail.save()
    return redirect("mailing:index")


@login_required
def important_return(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.important = False
    mail.save()
    return redirect("mailing:index")

@login_required
def trash_throw_away(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.garbage = True
    mail.save()
    return redirect("mailing:index")

    
@login_required
def trash_return(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.garbage = False
    mail.save()
    return redirect("mailing:bin")
