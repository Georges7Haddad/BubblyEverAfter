from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from inventory.decorators import user_is_item_creator
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
            item = form.save()
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
            item = form.save()
            category = Category.objects.get(pk=category_id)
            category.items.add(item)
            category.save()
            return redirect("inventory:index")
        else:
            return render(request, "inventory/AddItem.html", {"form": form})
    else:
        form = AddElectricalItemForm()
        return render(request, "inventory/AddItem.html", {"form": form})


@user_is_item_creator
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


@user_is_item_creator
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


@user_is_item_creator
def delete_item(request, item_id):
    Item.objects.filter(pk=item_id).delete()
    return redirect("inventory:index")
