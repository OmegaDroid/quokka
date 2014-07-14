from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def img_tag(obj, cls=""):
    if hasattr(obj, "img"):
        if obj.img:
            return mark_safe("<img class='" + cls + "' src='" + obj.img.url + "'/>")
    return mark_safe("<span class='glyphicon glyphicon-picture " + cls + "'></span>")


@register.filter
def concat(obj, other):
    try:
        return str(obj) + str(other)
    except:
        return ""


@register.filter
def object_link(obj):
    try:
        return ("/" + type(obj).__name__ + "/" + str(obj.id) + "/").lower()
    except:
        return ""


@register.filter
def object_anchor(obj):
    return mark_safe("<a href='" + object_link(obj) + "'>" + str(obj) + "</a>")
