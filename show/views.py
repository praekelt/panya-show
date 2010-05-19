from cal.models import EntryItem
from cal.pagemenus import EntriesByWeekdaysPageMenu
from content.generic.views import GenericObjectList
from content.models import ModelBase
from show.models import RadioShow, ShowContributor

class RadioShowContributorURL(object):
    def __call__(self, obj):
        contributors = obj.get_primary_contributors()
        if contributors:
            return contributors[0].get_absolute_url()
        else:
            ''

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
    
    def get_url_callable(self):
        return RadioShowContributorURL()

radioshow_entryitem_list = RadioShowEntryItemList()

class ShowContributorDetail(GenericObjectList):
    def get_extra_context(self, slug, *args, **kwargs):
        extra_context = super(ShowContributorDetail, self).get_extra_context(*args, **kwargs)
        added_context = {
            'title': 'DJS & Shows',
            'contributor': ShowContributor.permitted.get(slug=slug)
        }
        if extra_context:
            extra_context.update(
                added_context,
            )
        else:
            extra_context = added_context

        return extra_context
   
    def get_template_name(self):
        return 'show/showcontributor_detail.html'
    
    def get_pagemenu(self, request, queryset):
        return None
        return  EntriesByWeekdaysPageMenu(queryset=queryset, request=request)

    def get_queryset(self, slug):
        owner = ShowContributor.permitted.get(slug=slug).owner
        if owner:
            return ModelBase.permitted.filter(owner=owner).order_by('created')
        else:
            return ModelBase.permitted.exclude(owner=owner)
    
    def get_url_callable(self):
        return RadioShowContributorURL()

showcontributor_detail = ShowContributorDetail()
