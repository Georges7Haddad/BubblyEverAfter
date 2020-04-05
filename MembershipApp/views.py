from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import BubblyMember


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            credentials = form.cleaned_data
            username = credentials["username"]
            password = credentials["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                user = User.objects.get(username=username)
                member = BubblyMember.objects.get(user=user.id)
                if member.is_leadership:
                    return redirect("/member/leader/profile")
                else:
                    return redirect("/member/profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="Membership/members_login.html", context={"form": form})


@login_required(login_url="/member/login")
def member_profile(request):
    return render(request, "Membership/member_profile.html")


@login_required(login_url="/member/login")
def leader_profile(request):
    return render(request, "Membership/leader_profile.html")
