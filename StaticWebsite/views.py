from django.contrib import messages
from django.shortcuts import render, redirect

from MembershipApp.forms import ContactForm, CreateEvent
from MembershipApp.models import BubblyEvent


def index(request):
    return render(request, "MembershipApp/static_website/home.html")


def burningman(request):
    return render(request, "MembershipApp/static_website/burningman.html")


def legal(request):
    return render(request, "MembershipApp/static_website/community_ethos.html")


def about(request):
    return render(request, "MembershipApp/static_website/about.html")


def terms_and_conditions(request):
    return render(request, "MembershipApp/static_website/terms_and_conditions.html")


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect("/home")
        else:
            return render(
                request=request, template_name="MembershipApp/static_website/contact.html",
                context={"contact_form": contact_form},
            )

    contact_form = ContactForm()
    return render(request, "MembershipApp/static_website/contact.html", context={"contact_form": contact_form})


def display_events(request):
    events = BubblyEvent.objects.all()
    context = {"events": events}
    return render(request, "MembershipApp/static_website/display_events.html", context)


def create_event(request):
    if request.method == "POST":
        event_form = CreateEvent(request.POST)
        if event_form.is_valid():
            event_form.save()
            return redirect("/display_events")
        else:
            messages.warning(request, "Please fill all fields appropriately ")
            return render(
                request=request, template_name="MembershipApp/static_website/createvent.html",
                context={"CreateEvent": CreateEvent},
            )

    event_form = CreateEvent()
    return render(request, "MembershipApp/static_website/createvent.html", context={"event_form": event_form})
