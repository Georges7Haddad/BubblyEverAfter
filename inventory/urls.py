from django.urls import path
from .views import *

app_name = 'inventory'
urlpatterns = [
    path("",index, name="index"),
    path('<int:category_id>/',Display_Category, name="Display_Category"),
    path('<int:category_id>/add/', Add_Item, name="Add_Item"),
    path('edit/<int:item_id>', Edit_Item, name="Edit_Item"),
    path('delete/<int:item_id>', Delete_Item, name="Delete_Item")
]