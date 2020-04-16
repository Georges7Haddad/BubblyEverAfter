from django.shortcuts import render, redirect

from MembershipApp.forms import ContactForm


def index(request):
    return render(request, 'MembershipApp/index.html')


def burningman(request):
    return render(request, 'MembershipApp/burningman.html')


def legal(request):
    return render(request, 'MembershipApp/community_ethos.html')


def about(request):
    return render(request, 'MembershipApp/about.html')


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect("/home")
        else:
            return render(
                request=request,
                template_name="MembershipApp/contact.html",
                context={"contact_form": contact_form},
            )

    contact_form = ContactForm()
    return render(request, "MembershipApp/contact.html", context={"contact_form": contact_form})
