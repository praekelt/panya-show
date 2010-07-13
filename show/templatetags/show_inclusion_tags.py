from django import template

from show.models import Show

register = template.Library()

@register.inclusion_tag('show/inclusion_tags/radioshow_entryitem_listing.html', takes_context=True)
def radioshow_entryitem_listing(context, object_list):
    context.update({'object_list': object_list})
    return context

@register.inclusion_tag('show/inclusion_tags/showcontributor_header.html')
def showcontributor_header(obj):
    from cal.models import Entry
    # get entries for the shows the contributor contributes to.
    shows = Show.objects.filter(contributor=obj)
    modelbase_objs = [show.modelbase_obj for show in shows]
    entries = Entry.objects.filter(content__in=modelbase_objs)

    return {
        'entries': entries,
        'object': obj
    }

@register.inclusion_tag('show/inclusion_tags/showcontributor_detail.html')
def showcontributor_detail(obj):
    return {'object': obj}
