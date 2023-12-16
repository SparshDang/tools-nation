import os
from django.template import Library


register = Library()

@register.filter()
def get_base_name(path):
    return os.path.basename(path)