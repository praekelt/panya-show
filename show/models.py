from django.conf import settings
from django.db import models

from content.models import ModelBase
from options.models import Options

# Content Models
class CastMember(ModelBase):
    profile = models.TextField(help_text='Full profile for this castmember.')
    shows = models.ManyToManyField(
        'show.Show', 
        through='show.Credit'
    )

    class Meta:
        verbose_name = 'Cast Member'
        verbose_name_plural = 'Cast Members'

class Credit(models.Model):
    castmember = models.ForeignKey(
        'show.CastMember', 
        related_name='credits'
    )
    show = models.ForeignKey(
        'show.Show', 
        related_name='credits'
    )
    role = models.CharField(
        max_length=255, 
        blank=True, 
        null=True)

    def __unicode__(self):
        return "%s credit for %s" % (self.castmember.title, self.show.title)

class Show(ModelBase):
    content = models.TextField(
        help_text="Full article detailing this show.",
        blank=True,
        null=True,
    )
    castmembers = models.ManyToManyField(
        'show.CastMember', 
        through='show.Credit'
    )

class RadioShow(Show):
    pass

# Option Models
class ShowOptions(Options):
    __module__ = 'options.models'

    class Meta():
        verbose_name = 'Show Options'
        verbose_name_plural = 'Show Options'

class CreditOption(models.Model):
    show_options = models.ForeignKey('options.ShowOptions')
    role_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    role_priority = models.IntegerField(
        blank=True,
        null=True,
    )
