from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import MatButtonModel, MatChipTagModel


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

plugin_pool.register_plugin(MatButton)
plugin_pool.register_plugin(MatChipTag)