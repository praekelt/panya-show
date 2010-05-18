from cal.models import EntryItem
from content.generic.views import GenericObjectList 
from show.models import RadioShow

class RadioShowEntryItemList(GenericObjectList):
    def get_extra_context(self, *args, **kwargs):
        extra_context = super(RadioShowEntryItemList, self).get_extra_context(*args, **kwargs)
        added_context = {'title': 'DJS & Shows'}
        if extra_context:
            extra_context.update(
                added_context,
            )
        else:
            extra_context = added_context

        return extra_context
    
    def get_template_name(self):
        return 'show/radioshow_entryitem_list.html'
    
    def get_filterset(self, request, queryset):
        return None
    
    def get_queryset(self):
        return EntryItem.permitted.by_model(RadioShow)#.this_week().order('start')

radioshow_entryitem_list = RadioShowEntryItemList()
