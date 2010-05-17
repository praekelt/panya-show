from django.conf import settings
from django.db import models

from ckeditor.fields import RichTextField
from content.models import ModelBase
from options.models import Options

# Content Models
class Contributor(ModelBase):
    profile = RichTextField(help_text='Full profile for this castmember.')
    shows = models.ManyToManyField(
        'show.Show', 
        through='show.Credit',
        related_name='show_contributors',
    )

    class Meta:
        verbose_name = 'Contributor'
        verbose_name_plural = 'Contributors'

class Credit(models.Model):
    contributor = models.ForeignKey(
        'show.Contributor', 
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
    content = RichTextField(
        help_text="Full article detailing this show.",
        blank=True,
        null=True,
    )
    contributor = models.ManyToManyField(
        'show.Contributor', 
        through='show.Credit',
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
