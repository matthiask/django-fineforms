from __future__ import absolute_import, unicode_literals

from django import forms, template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import html_safe, mark_safe
from django.utils.translation import ugettext as _


register = template.Library()


# TODO aria-describedby etc.


@html_safe
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

    def __str__(self):
        return render_to_string(self.template_name, {
            'top_errors': self.top_errors,
            'has_field_errors': self.has_field_errors,
        })


@html_safe
class FieldWrapper(object):
    template_name = 'fineforms/field.html'

    def __init__(self, field):
        self.field = field

    def __str__(self):
        return render_to_string(self.template_name, {
            'field': self.field,
            'widget_then_label': isinstance(
                self.field.field.widget,
                forms.CheckboxInput,
            ),
        })


class PlainFieldWrapper(FieldWrapper):
    template_name = 'fineforms/field-plain.html'


@html_safe
class FieldsWrapper(object):
    template_name = 'fineforms/fields.html'

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields

    def __str__(self):
        bfs = [self.form[field] for field in self.fields]
        return render_to_string(self.template_name, {
            'fields': [
                FINEFORMS_WRAPPERS['field'](bf) for bf in bfs
                if not bf.is_hidden
            ],
            'hidden': mark_safe(''.join(
                str(bf) for bf in bfs if bf.is_hidden
            )),
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
