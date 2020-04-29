from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_element(array, index):
    return array[index]


@register.filter
def get_attribute(obj, attr):
    return getattr(obj, attr)
