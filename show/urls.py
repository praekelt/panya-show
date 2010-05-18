from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'show.views',
    url(r'^radioshow/entrylist/$', 'radioshow_entryitem_list', name='radioshow_entryitem_list'),
)
