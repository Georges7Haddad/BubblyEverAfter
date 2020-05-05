from django.core.exceptions import PermissionDenied

from inventory.models import *


def user_is_item_creator(function):
    def wrap(request, item_id):
        item = Item.objects.get(pk=item_id)
        if item.member == request.user:
            return function(request, item_id)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
