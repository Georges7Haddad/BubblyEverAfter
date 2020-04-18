from django.urls import path
from .views import *

app_name = "inventory"
urlpatterns = [
    path("", index, name="index"),
    path("<int:category_id>/", display_category, name="display_category"),
    path("<int:category_id>/add/", add_item, name="add_item"),
    path("<int:category_id>/addElectric/", add_electrical_item, name="add_electrical_item"),
    path("edit/<int:item_id>", edit_item, name="edit_item"),
    path("editElectric/<int:item_id>", edit_electrical_item, name="edit_electrical_item"),
    path("delete/<int:item_id>", delete_item, name="delete_item"),
]
