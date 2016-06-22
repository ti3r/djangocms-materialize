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

MAT_CARD_SIZE_CHOICES = (
    ("small",_("Small")),
    ("medium",_("Medium")),
    ("large",_("Large")),
)

MAT_CARD_CONTENT_MODES = (
    ("content",_("Content")),
    ("action",_("Action")),
    ("image", _("Image")),
    ("reveal",_("Reveal (Experimental)")),
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
        #elif self.link_file:
        #    link = self.link_file.url
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
        clazz = u''
        if self.mode == 'F1':
            clazz = u'btn-floating'
        elif self.mode == 'F2':
            clazz = u'btn-flat'
        elif self.large:
            clazz = u'btn-large'
        else:
            clazz = u'btn'
        clazz += ' {ec}'.format(ec=self.extra_classes)
        return clazz

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


class MatCardModel(CMSPlugin):
    """
    Model class to store the configuration of the Card plugin.
    """
    size = models.CharField(max_length=100, default='small', blank=True, null=True, verbose_name=_('Size'),
                            choices=MAT_CARD_SIZE_CHOICES)
    is_panel = models.BooleanField(default=False, verbose_name=_("Is Panel"),
                                    help_text=_("Mark this card panel (more simple card component). More info see: \
                                    http://materializecss.com/cards.html"))
    extra_classes = models.TextField(null=True, blank=True,
                                     help_text=_('Add extra class names that you wish to add to the component')
                                     , verbose_name=_('Extra Classes'))

    def get_card_classes(self):
        classes = u'card'
        if self.is_panel:
            classes += u'-panel'
        classes += ' {size} '.format(size=self.size)
        classes += ' {ec} '.format(ec=self.extra_classes)
        return classes


class MatCardContentModel(CMSPlugin):
    """
    Model class to store the configuration of the different card contents
    """
    title = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=_('Title'))
    mode = models.CharField(default='', verbose_name=_("Mode"), choices=MAT_CARD_CONTENT_MODES, max_length=20,
                                    help_text=_("Mark the style of the content. More info see: \
                                    http://materializecss.com/cards.html"))
    extra_classes = models.TextField(null=True, blank=True,
                                     help_text=_('Add extra class names that you wish to add to the component')
                                     , verbose_name=_('Extra Classes'))

    def get_content_class(self):
        """
        returns the class that should be applied to the card content row based on the different flags for the plugin.
        :return: unicode materialize class name
        """
        clazz = u'card-{mode}'
        if self.mode:
            clazz = clazz.format(mode=self.mode)
        else:
            clazz = clazz.format(mode='content')
        return clazz

    def get_extra_classes(self):
        """
        returns the list of extra class names that should be applied to the card content template
        :return:
        """
        return self.extra_classes