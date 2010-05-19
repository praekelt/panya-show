from cal.models import EntryItem
from cal.pagemenus import EntriesByWeekdaysPageMenu
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
    
    def get_pagemenu(self, request, queryset):
        return  EntriesByWeekdaysPageMenu(queryset=queryset, request=request)
    
    def get_queryset(self):
        return EntryItem.permitted.by_model(RadioShow).order_by('start')

radioshow_entryitem_list = RadioShowEntryItemList()
