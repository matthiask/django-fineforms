from __future__ import absolute_import, unicode_literals

from django import template
from django.utils.html import mark_safe

from fineforms.wrappers import FINEFORMS_WRAPPERS


register = template.Library()


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
