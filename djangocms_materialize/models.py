from cms.models.pluginmodel import CMSPlugin

from django.db import models
from filer.fields.image import FilerImageField
from django.utils.translation import ugettext_lazy as _
from cms.models import fields

MAT_BUTTON_MODE_CHOICES = (
    ('N', _('NORMAL')),
    ('F1', _('FLOAT')),
    ('F2', _('FLAT'))
)

MAT_BUTTON_TARGET_CHOICES = (
            ("", _("same window")),
            ("_blank", _("new window")),
            ("_parent", _("parent window")),
            ("_top", _("topmost frame")),
)

MAT_BUTTON_ICON_POSITION_CHOICES = (
    ("left", _("Left")),
    ("right", _("Right")),
)

##########
# Mixins #
##########
class ButtonMixin(models.Model):
    link_url = models.URLField(_("link"), blank=True, default='')
    link_page = fields.PageField(verbose_name=_("Page"), blank=True, null=True, on_delete=models.SET_NULL)
    #link_file = filer.fields.file.FilerFileField(
    #    verbose_name=_("file"),
    #    null=True,
    #    blank=True,
    #    on_delete=models.SET_NULL,
    #)
    link_anchor = models.CharField(_("anchor"), max_length=128, blank=True,
                                   help_text=_("Adds this value as an anchor (#my-anchor) to the link."),)
    link_mailto = models.EmailField(_("mailto"), blank=True, null=True, max_length=254)
    link_phone = models.CharField(_('Phone'), blank=True, null=True, max_length=40,)
    link_target = models.CharField(_("target"), blank=True, max_length=100, choices= MAT_BUTTON_TARGET_CHOICES)

    class Meta:
        abstract = True

    def get_link_url(self):
        if self.link_phone:
            link = u"tel://{0}".format(self.link_phone).replace(' ', '')
        elif self.link_mailto:
            link = u"mailto:{0}".format(self.link_mailto)
        elif self.link_url:
            link = self.link_url
        elif self.link_page_id:
            link = self.link_page.get_absolute_url()
        elif self.link_file:
            link = self.link_file.url
        else:
            link = ""
        if self.link_anchor:
            link += '#{0}'.format(self.link_anchor)
        return link

class MatButtonModel(CMSPlugin, ButtonMixin):
    """
    Model to store the configuration of the button plugin.
    """
    caption = models.CharField(max_length=100, default='', blank=True, null=True,)
    mode = models.CharField(default='', null=True, choices= MAT_BUTTON_MODE_CHOICES, max_length=10)
    disabled = models.BooleanField(default=False)
    large = models.BooleanField(default=False)
    extra_classes = models.TextField(null=True, blank=True,
                                     help_text=_('Add extra class names that you wish to add to the component')
                                     , verbose_name=_('Extra Classes'))
    icon = models.CharField(null=True, blank=True, verbose_name=_('Icon Name'), max_length=100,
                            help_text=_('Add the name of the material icon you wish to display. See Material Icons.'))
    icon_position = models.CharField(null=True, blank=True, verbose_name=_('Icon Position'), max_length=100
                                     ,choices=MAT_BUTTON_ICON_POSITION_CHOICES)

    def get_btn_class(self):
        if self.mode == 'F1':
            return u'btn-floating'
        elif self.mode == 'F2':
            return u'btn-flat'
        elif self.large:
            return u'btn-large'
        else:
            return u'btn'

    def is_disabled(self):
        return u'disabled' if self.disabled else u''


class MatChipTagModel(CMSPlugin):
    """
    Model class to store the configuration of the Chip/Tag plugin.
    """
    caption = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=_('Caption'))
    image = FilerImageField(verbose_name=_('Image'), blank=True, null=True, on_delete=models.SET_NULL)
    image_alt = models.CharField(max_length=100,default='', blank=True, null=True,
                                 verbose_name=_('Alternate text for image'))
    is_tag = models.BooleanField(default=False, verbose_name=_('Is a Tag'))

