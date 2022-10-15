from django import template
from django.utils import timezone

register = template.Library()


def absolute(value):
    return abs(value)
