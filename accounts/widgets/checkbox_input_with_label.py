from django.utils.html import format_html
from django.forms.widgets import CheckboxInput
import re

class CheckboxInputWithLabel(CheckboxInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        label_text = self.attrs.pop('label', 'Label')
        checkbox_html = super().render(name, value, attrs, renderer)
        template = '<div class="form-check mb-3">{checkbox}<label class="form-check-label" for="{id}">{label}</label></div>'
        return format_html(template, checkbox=checkbox_html, id=attrs.get('id', name), label=label_text)
