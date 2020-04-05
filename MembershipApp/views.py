from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import BubblyMemberForm
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


def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        bubbly_form = BubblyMemberForm(request.POST)
        if user_form.is_valid() and bubbly_form.is_valid():
            saving_user = user_form.save()
            user_data = user_form.cleaned_data
            user = User.objects.get(username=user_data["username"])
            bubblymember = bubbly_form.cleaned_data
            BubblyMember.objects.create(
                user=user,
                birthday=bubblymember["birthday"],
                gender_identity=bubblymember["gender_identity"],
                ethnic_identity=bubblymember["ethnic_identity"],
                country=bubblymember["country"],
                city=bubblymember["city"],
                photo=bubblymember["photo"],
                facebook=bubblymember["facebook"],
                phone_number=bubblymember["phone_number"],
                paypal_email=bubblymember["paypal_email"],
                playa_name=bubblymember["playa_name"],
                burning_man_profile_email=bubblymember["burning_man_profile_email"],
                is_virgin_burner=bubblymember["is_virgin_burner"],
                years_attending_burning_man=bubblymember["years_attending_burning_man"],
                referring_member=bubblymember["referring_member"],
                allergies=bubblymember["allergies"],
                medical_issues=bubblymember["medical_issues"],
            )
            login(request, saving_user)
            return redirect("/member/profile")
        else:
            for msg in user_form.error_messages or bubbly_form.error_messages:
                print(user_form.error_messages[msg] or bubbly_form.error_messages[msg])
                return render(
                    request=request,
                    template_name="Membership/member_register.html",
                    context={"user_form": user_form, "bubbly_form": bubbly_form},
                )

    user_form = UserCreationForm()
    bubbly_form = BubblyMemberForm()
    return render(
        request, "Membership/member_register.html", context={"user_form": user_form, "bubbly_form": bubbly_form}
    )
