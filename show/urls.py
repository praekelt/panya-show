from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'show.views',
    url(r'^radioshow/entrylist/$', 'radioshow_entryitem_list', name='radioshow_entryitem_list'),
    url(r'^showcontributor/list/(?P<slug>[\w-]+)/$', 'showcontributor_content_list', name='showcontributor_content_list'),
    url(r'^showcontributor/appearance/(?P<slug>[\w-]+)/$', 'showcontributor_appearance_list', name='showcontributor_appearance_list'),
    url(r'^showcontributor/(?P<slug>[\w-]+)/$', 'showcontributor_detail', name='showcontributor_detail'),
    url(r'^showcontributor/content/(?P<slug>[\w-]+)/$', 'showcontributor_content_detail', name='showcontributor_content_detail'),
)
