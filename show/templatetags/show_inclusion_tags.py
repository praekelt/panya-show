from django import template

register = template.Library()

@register.inclusion_tag('show/inclusion_tags/radioshow_entryitem_listing.html')
def radioshow_entryitem_listing(object_list):
    return {'object_list': object_list}
