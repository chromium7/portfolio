from django import template
from django.utils.safestring import SafeString, mark_safe
from markdownx.utils import markdownify as markdownx_markdownify

register = template.Library()


@register.filter(name="markdownify")
def markdownify(content: str) -> SafeString:
    return mark_safe(markdownx_markdownify(content))
