from __future__ import absolute_import, unicode_literals

from django import forms, template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


register = template.Library()


# TODO aria-describedby etc.


class ErrorsWrapper(object):
    template_name = 'fineforms/errors.html'

    def __init__(self, forms):
        self.forms = forms
        self.top_errors = []
        self.has_field_errors = False
        for form in self.forms:
            self.top_errors.extend(form.non_field_errors())
            for name in form.fields:
                bf = form[name]
                if bf.is_hidden and bf.errors:
                    self.top_errors.extend([
                        _('(Hidden field %(name)s) %(error)s') % {
                            'name': name,
                            'error': e,
                        } for e in bf.errors
                    ])

                if bf.errors:
                    self.has_field_errors = True

    def __html__(self):
        return render_to_string(self.template_name, {
            'wrapper': self,
        })


class FieldWrapper(object):
    template_name = 'fineforms/field.html'

    def __init__(self, field):
        self.field = field

    def widget_then_label(self):
        return isinstance(self.field.field.widget, forms.CheckboxInput)

    def __html__(self):
        return render_to_string(self.template_name, {
            'wrapper': self,
            'field': self.field,
        })


class PlainFieldWrapper(FieldWrapper):
    template_name = 'fineforms/field-plain.html'


class FieldsWrapper(object):
    template_name = 'fineforms/fields.html'

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields

    def __html__(self):
        return render_to_string(self.template_name, {
            'wrapper': self,
            'fields': [
                FINEFORMS_WRAPPERS['field'](field)
                for field in self.fields
            ],
        })


@register.simple_tag
def ff_errors(*forms):
    return FINEFORMS_WRAPPERS['errors']([form for form in forms if form])


@register.simple_tag
def ff_field(field, type='field'):
    return FINEFORMS_WRAPPERS[type](field)


@register.simple_tag
def ff_fields(form, fields=None, exclude=None):
    if fields is not None:
        fields = fields.split(',')
    elif exclude is not None:
        exclude = exclude.split(',')
        fields = [
            f for f in list(form.fields) if f not in exclude
        ]
    else:
        fields = list(form.fields)

    for f in fields:
        return FINEFORMS_WRAPPERS['fields'](form, fields)


@register.simple_tag
def ff_hidden_fields(*forms):
    fields = []
    for form in [f for f in forms if f]:
        for name in form.fields:
            bf = form[name]
            if bf.is_hidden:
                fields.append(bf)
    return mark_safe(''.join(str(f) for f in fields))


FINEFORMS_WRAPPERS = {
    'errors': ErrorsWrapper,
    'field': FieldWrapper,
    'fields': FieldsWrapper,
    'field-plain': PlainFieldWrapper,
}
FINEFORMS_WRAPPERS.update(getattr(settings, 'FINEFORMS_WRAPPERS', {}))
