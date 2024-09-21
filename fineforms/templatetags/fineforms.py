from django import template
from django.utils.html import mark_safe

from fineforms.wrappers import wrapper


register = template.Library()


@register.simple_tag
def ff_errors(*forms, **kwargs):
    return wrapper("errors")([form for form in forms if form], **kwargs)


@register.simple_tag
def ff_field(field, type="field", **kwargs):
    return wrapper(type)(field, **kwargs)


@register.simple_tag
def ff_fields(form, fields=None, exclude=None, **kwargs):
    if fields is not None:
        fields = fields.split(",")
    elif exclude is not None:
        exclude = exclude.split(",")
        fields = [f for f in list(form.fields) if f not in exclude]
    else:
        fields = list(form.fields)

    return wrapper("fields")(form, fields, **kwargs)


@register.simple_tag
def ff_hidden_fields(*forms):
    fields = []
    for form in [f for f in forms if f]:
        for name in form.fields:
            bf = form[name]
            if bf.is_hidden:
                fields.append(bf)
    return mark_safe("".join(str(f) for f in fields))


@register.inclusion_tag("fineforms/submit.html")
def ff_submit(text=None):
    return {"text": text}
