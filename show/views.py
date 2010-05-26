from django.core.urlresolvers import reverse

from cal.models import EntryItem
from cal.pagemenus import EntriesByWeekdaysPageMenu
from content.generic.views import GenericObjectDetail, GenericObjectList
from content.models import ModelBase
from event.models import Appearance, Event
from show.models import RadioShow, ShowContributor
from show.pagemenus import ShowContributorPageMenu

class ShowContributerContentURL(object):
    def __call__(self, obj):
        return reverse('showcontributor_content_detail', kwargs={'slug': obj.slug})

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
    
    def get_pagemenu(self, request, queryset, *args, **kwargs):
        return  EntriesByWeekdaysPageMenu(queryset=queryset, request=request)
    
    def get_queryset(self):
        return EntryItem.permitted.by_model(RadioShow).order_by('start')
    
radioshow_entryitem_list = RadioShowEntryItemList()

class ShowContributorContentList(GenericObjectList):
    def get_extra_context(self, slug, *args, **kwargs):
        extra_context = super(ShowContributorContentList, self).get_extra_context(*args, **kwargs)
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
        return 'show/showcontributor_content_list.html'
    
    def get_url_callable(self):
        return ShowContributerContentURL()
    
    def get_pagemenu(self, request, queryset, slug, *args, **kwargs):
        return ShowContributorPageMenu(queryset=queryset, request=request, slug=slug)
    
    def get_paginate_by(self):
        return 7

    def get_queryset(self, slug):
        owner = ShowContributor.permitted.get(slug=slug).owner
        if owner:
            return ModelBase.permitted.filter(owner=owner).exclude(class_name__in=["ShowContributor",]).order_by('created')
        else:
            return ModelBase.permitted.exclude(owner=owner)
    
showcontributor_content_list = ShowContributorContentList()

class ShowContributorDetail(GenericObjectDetail):
    def get_template_name(self):
        return 'show/showcontributor_detail.html'
    
    def get_pagemenu(self, request, queryset, slug, *args, **kwargs):
        return ShowContributorPageMenu(queryset=queryset, request=request, slug=slug)
    
    def get_queryset(self, *args, **kwargs):
        return ShowContributor.permitted.all()

showcontributor_detail =  ShowContributorDetail()

class ShowContributorContentDetail(GenericObjectDetail):
    def get_template_name(self):
        return 'show/showcontributor_content_detail.html'
    
    def get_contributor(self, slug):
        return self.get_queryset().get(slug=slug).owner.modelbase_set.get(class_name='ShowContributor')

    def get_pagemenu(self, request, queryset, slug, *args, **kwargs):
        return ShowContributorPageMenu(queryset=queryset, request=request, slug=self.get_contributor(slug).slug)
    
    def get_queryset(self, *args, **kwargs):
        return ModelBase.permitted.all()
    
    def get_extra_context(self, slug, *args, **kwargs):
        extra_context = super(ShowContributorContentDetail, self).get_extra_context(*args, **kwargs)
        added_context = {
            'title': 'DJS & Shows',
            'contributor': self.get_contributor(slug),
        }
        if extra_context:
            extra_context.update(
                added_context,
            )
        else:
            extra_context = added_context

        return extra_context
    
showcontributor_content_detail =  ShowContributorContentDetail()

class ShowContributorAppearanceList(GenericObjectList):
    def get_extra_context(self, slug, *args, **kwargs):
        extra_context = super(ShowContributorAppearanceList, self).get_extra_context(*args, **kwargs)
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
        return 'show/showcontributor_appearance_list.html'
    
    def get_url_callable(self):
        return None
    
    def get_pagemenu(self, request, queryset, slug, *args, **kwargs):
        return ShowContributorPageMenu(queryset=queryset, request=request, slug=slug)
    
    def get_paginate_by(self):
        return 7

    def get_queryset(self, slug):
        contributor = ShowContributor.permitted.get(slug=slug)
        if contributor:
            return EntryItem.permitted.by_model(Event).filter(
                content__in=Event.objects.filter(appearances__show_contributor=contributor)
            ).order_by('start')
        return []
    
showcontributor_appearance_list = ShowContributorAppearanceList()
