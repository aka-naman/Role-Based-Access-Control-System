from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Get item from dictionary by key.
    Usage in template: {{ record.data|get_item:column_name }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, None)
    return None


@register.filter
def slugify_custom(value):
    """
    Custom slugify that removes special characters for CSS class names.
    """
    if not value:
        return ''
    return str(value).lower().replace(' ', '-').replace('/', '-').replace('.', '-')
