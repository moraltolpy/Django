from django import template
from article.models import *

register = template.Library()

@register.simple_tag(name='gettypes')
def get_types(filter=None):
    if not filter:
        return Worktype.objects.all()
    else:
        return Worktype.objects.filter(pk=filter)
