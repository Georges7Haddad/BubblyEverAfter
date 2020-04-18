from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from inventory.forms import *
from inventory.models import Item, Category, ElectricalItem


def index(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "inventory/index.html", context)


def display_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    header = "Currently Viewing " + category.name
    context = {
        "items": category.items.all().select_related("electricalitem"),
        "name": category.name,
        "header": header,
        "category_id": category_id,
        "category": category,
    }
    return render(request, "inventory/DisplayCategory.html", context)


def add_item(request, category_id):
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            member = form.cleaned_data["member"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            width = form.cleaned_data["width"]
            height = form.cleaned_data["height"]
            length = form.cleaned_data["length"]
            quantity = form.cleaned_data["quantity"]
            unit_price = form.cleaned_data["unit_price"]
            picture = form.cleaned_data["picture"]
            # item = Item(member=member,title=title,description=description,width=width,height=height,length=length,quantity=quantity,unit_price=unit_price,picture=picture)
            # item.save()
            item = Item.objects.create(
                member=member,
                title=title,
                description=description,
                width=width,
                height=height,
                length=length,
                quantity=quantity,
                unit_price=unit_price,
                picture=picture,
            )
            item.save()
            category = Category.objects.get(pk=category_id)
            category.items.add(item)
            category.save()
            return redirect("inventory:index")
        else:
            return render(request, "inventory/AddItem.html", {"form": form})
    else:
        form = AddItemForm()
        return render(request, "inventory/AddItem.html", {"form": form})


def add_electrical_item(request, category_id):
    if request.method == "POST":
        form = AddElectricalItemForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            member = form.cleaned_data["member"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            width = form.cleaned_data["width"]
            height = form.cleaned_data["height"]
            length = form.cleaned_data["length"]
            quantity = form.cleaned_data["quantity"]
            unit_price = form.cleaned_data["unit_price"]
            picture = form.cleaned_data["picture"]
            voltage = form.cleaned_data["voltage"]
            wattage = form.cleaned_data["wattage"]
            # item = Item(member=member,title=title,description=description,width=width,height=height,length=length,quantity=quantity,unit_price=unit_price,picture=picture)
            # item.save()
            item = ElectricalItem.objects.create(
                member=member,
                title=title,
                description=description,
                width=width,
                height=height,
                length=length,
                quantity=quantity,
                unit_price=unit_price,
                picture=picture,
                voltage=voltage,
                wattage=wattage,
            )
            item.save()
            category = Category.objects.get(pk=category_id)
            category.items.add(item)
            category.save()
            return redirect("inventory:index")
        else:
            return render(request, "inventory/AddItem.html", {"form": form})
    else:
        form = AddElectricalItemForm()
        return render(request, "inventory/AddItem.html", {"form": form})


def edit_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:index")
        else:
            return render(request, "inventory/EditItem.html", {"form": form})
    else:
        form = AddItemForm(instance=item)
        return render(request, "inventory/EditItem.html", {"form": form})


def edit_electrical_item(request, item_id):
    item = ElectricalItem.objects.get(pk=item_id)
    if request.method == "POST":
        form = AddElectricalItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:index")
        else:
            return render(request, "inventory/EditItem.html", {"form": form})
    else:
        form = AddElectricalItemForm(instance=item)
        return render(request, "inventory/EditItem.html", {"form": form})


def delete_item(request, item_id):
    Item.objects.filter(pk=item_id).delete()
    return redirect("inventory:index")
