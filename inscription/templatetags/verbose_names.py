# Pour avoir accès à verbose_name de nos fields depuis le template
# https://stackoverflow.com/questions/14496978/fields-verbose-name-in-templates
# https://docs.djangoproject.com/en/dev/howto/custom-template-tags/
from django import template
register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name