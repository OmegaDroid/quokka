from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def img_tag(obj, cls=""):
    if hasattr(obj, "img"):
        if obj.img:
            return mark_safe("<img class='"+cls+"' src='"+obj.img.url+"'/>")
    return mark_safe("<span class='glyphicon glyphicon-picture "+cls+"'></span>")