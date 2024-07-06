from django import template

register = template.Library()

@register.filter(name='split_folder_name')
def split_folder_name(value):
    parts = value.rsplit('_', 1)  # Split from the right at the first underscore
    return parts[0] if parts else value

@register.filter(name='split_file_name')
def split_file_name(value):
    parts = value.rsplit('_', 1)
    return parts[0]+".xlsx" if parts else value

@register.filter(name='split_user_name')
def split_user_name(value):
    parts = value.rsplit('@', 1)
    return parts[0] if parts else value
