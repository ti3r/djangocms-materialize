from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import MatButtonModel, MatChipTagModel, MatCardContentModel, MatCardModel


class MatButton(CMSPluginBase):
    """
    Plugin to display a materialize button in the page
    """
    module = _("Materialize")
    name = _("Button")
    render_template = 'djangocms_materialize/components/button.html'
    change_form_template = 'djangocms_materialize/components/edit_forms/button_edt_form.html'
    cache = True
    model = MatButtonModel

class MatChipTag(CMSPluginBase):
    """
    Plugin to display a materialize chip or tag component
    """
    module = _("Materialize")
    name = _("Chip / Tag")
    render_template = 'djangocms_materialize/components/chip-tag.html'
    cache = True
    model = MatChipTagModel

class MatCardContent(CMSPluginBase):
    """
    Plugin to add one row of content to a card
    """
    module = _("Materialize")
    name = _("Card Content")
    render_template = 'djangocms_materialize/components/card-content.html'
    cache = True
    require_parent = True
    parent_classes = ['MatCard']
    model = MatCardContentModel
    allow_children = True
    #child_classes = ['text']

class MatCard(CMSPluginBase):
    """
    Plugin to display a card component
    """
    module = _("Materialize")
    name = _("Card")
    render_template = 'djangocms_materialize/components/card.html'
    cache = True
    allow_children = True
    child_classes = ['MatCardContent']
    model = MatCardModel


plugin_pool.register_plugin(MatButton)
plugin_pool.register_plugin(MatChipTag)
plugin_pool.register_plugin(MatCardContent)
plugin_pool.register_plugin(MatCard)