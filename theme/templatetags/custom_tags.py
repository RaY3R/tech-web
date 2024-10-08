from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def url_active(context, viewname):
    request = context['request']
    current_path = request.path
    compare_path = reverse(viewname)
    if current_path == compare_path:
        return 'active'
    else:
        return ''