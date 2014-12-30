from django import template

from races.models import Season

register = template.Library()

@register.simple_tag
def current_season():
    "Return the current season."
    return Season.current_season.all()
