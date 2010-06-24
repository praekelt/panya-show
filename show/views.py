from django.core.urlresolvers import reverse

from cal.models import EntryItem
from cal.view_modifiers import EntriesByWeekdaysViewModifier
from panya.generic.views import GenericObjectDetail, GenericObjectList
from panya.models import ModelBase
from event.models import Event
from show.models import Appearance, RadioShow, ShowContributor
from show.view_modifiers import ShowContributorViewModifier

class ShowContributerContentURL(object):
    def __call__(self, obj=None):
        if obj:
            return reverse('showcontributor_content_detail', kwargs={'slug': obj.slug})
        else:
            return self

class RadioShowEntryItemList(GenericObjectList):
    def get_extra_context(self, *args, **kwargs):
        return  {'title': 'DJS & Shows'}
    
    def get_template_name(self, *args, **kwargs):
        return 'show/radioshow_entryitem_list.html'
    
    def get_view_modifier(self, request, *args, **kwargs):
        return  EntriesByWeekdaysViewModifier(request=request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        return EntryItem.permitted.by_model(RadioShow).order_by('start')
    
radioshow_entryitem_list = RadioShowEntryItemList()

class ShowContributorContentList(GenericObjectList):
    def get_extra_context(self, *args, **kwargs):
        slug = kwargs['slug']
        return {
            'title': 'DJS & Shows',
            'contributor': ShowContributor.permitted.get(slug=slug)
        }
   
    def get_template_name(self, *args, **kwargs):
        return 'show/showcontributor_content_list.html'
    
    def get_url_callable(self, *args, **kwargs):
        return ShowContributerContentURL()
    
    def get_view_modifier(self, request, slug, *args, **kwargs):
        return ShowContributorViewModifier(request=request, slug=slug, *args, **kwargs)
    
    def get_paginate_by(self, *args, **kwargs):
        return 7

    def get_queryset(self, *args, **kwargs):
        slug = kwargs['slug']
        owner = ShowContributor.permitted.get(slug=slug).owner
        if owner:
            return ModelBase.permitted.filter(owner=owner).exclude(class_name__in=["ShowContributor",]).order_by('created')
        else:
            return ModelBase.permitted.exclude(owner=owner)
    
showcontributor_content_list = ShowContributorContentList()

class ShowContributorDetail(GenericObjectDetail):
    def get_template_name(self, *args, **kwargs):
        return 'show/showcontributor_detail.html'
    
    def get_view_modifier(self, request, slug, *args, **kwargs):
        return ShowContributorViewModifier(request=request, slug=slug, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        return ShowContributor.permitted.all()
    
    def get_extra_context(self, *args, **kwargs):
        return {'title': 'DJS & Shows'}

showcontributor_detail =  ShowContributorDetail()

class ShowContributorContentDetail(GenericObjectDetail):
    def get_template_name(self, *args, **kwargs):
        return 'show/showcontributor_content_detail.html'
    
    def get_contributor(self, slug):
        return self.get_queryset().get(slug=slug).owner.modelbase_set.get(class_name='ShowContributor')

    def get_view_modifier(self, request, slug, *args, **kwargs):
        return ShowContributorViewModifier(request=request, slug=self.get_contributor(slug).slug, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        return ModelBase.permitted.all()
    
    def get_extra_context(self, *args, **kwargs):
        slug=kwargs['slug']
        return {
            'title': 'DJS & Shows',
            'contributor': self.get_contributor(slug),
        }
    
showcontributor_content_detail =  ShowContributorContentDetail()

class ShowContributorAppearanceList(GenericObjectList):
    def get_extra_context(self, *args, **kwargs):
        slug = kwargs['slug']
        return {
            'title': 'DJS & Shows',
            'contributor': ShowContributor.permitted.get(slug=slug)
        }
   
    def get_template_name(self, *args, **kwargs):
        return 'show/showcontributor_appearance_list.html'
    
    def get_view_modifier(self, request, slug, *args, **kwargs):
        return ShowContributorViewModifier(request=request, slug=slug, *args, **kwargs)
    
    def get_paginate_by(self, *args, **kwargs):
        return 7

    def get_queryset(self, *args, **kwargs):
        slug = kwargs['slug']
        contributor = ShowContributor.permitted.get(slug=slug)
        if contributor:
            return EntryItem.permitted.by_model(Event).filter(
                content__in=Event.objects.filter(appearances__show_contributor=contributor)
            ).order_by('start')
        return []
    
showcontributor_appearance_list = ShowContributorAppearanceList()
