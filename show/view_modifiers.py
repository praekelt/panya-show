from panya.view_modifiers import ViewModifier
from panya.view_modifiers.items import URLPatternItem
from django.core.urlresolvers import reverse

class ShowContributorViewModifier(ViewModifier):
    def __init__(self, request, slug, *args, **kwargs):
        self.items = [
            URLPatternItem(request, title="Blog", path=reverse('showcontributor_content_list', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_content_list', 'showcontributor_content_detail',], default=False),
            URLPatternItem(request, title="Profile", path=reverse('showcontributor_detail', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_detail',], default=False),
            #URLPatternItem(request, title="Contact", path=reverse('showcontributor_detail', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_detail',], default=False),
            URLPatternItem(request, title="Appearances", path=reverse('showcontributor_appearance_list', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_appearance_list',], default=False),
        ]
        super(ShowContributorViewModifier, self).__init__(request)
