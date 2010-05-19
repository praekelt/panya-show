from django import template

register = template.Library()

@register.inclusion_tag('show/inclusion_tags/radioshow_entryitem_listing.html', takes_context=True)
def radioshow_entryitem_listing(context, object_list):
    context.update({'object_list': object_list})
    return context
