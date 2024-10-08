from functools import cache

from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import html_safe, mark_safe
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _


# TODO aria-describedby etc.


@html_safe
class ErrorsWrapper:
    template_name = "fineforms/errors.html"

    def __init__(self, forms):
        self.forms = forms
        self.top_errors = []
        self.has_field_errors = False
        for form in self.forms:
            self.top_errors.extend(form.non_field_errors())
            for name in form.fields:
                bf = form[name]
                if bf.is_hidden and bf.errors:
                    self.top_errors.extend(
                        [
                            _("(Hidden field %(name)s) %(error)s")
                            % {"name": name, "error": e}
                            for e in bf.errors
                        ]
                    )

                if bf.errors:
                    self.has_field_errors = True

    def __str__(self):
        return render_to_string(
            self.template_name,
            {
                "forms": self.forms,
                "top_errors": self.top_errors,
                "has_field_errors": self.has_field_errors,
            },
        )


@html_safe
class FieldWrapper:
    template_name = "fineforms/field.html"
    label_suffix = ""
    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, field):
        self.field = field

    def __str__(self):
        extra_classes = []
        if not hasattr(self.field.form, "error_css_class") and self.field.errors:
            extra_classes.append(self.error_css_class)
        if (
            not hasattr(self.field.form, "required_css_class")
            and self.field.field.required
        ):
            extra_classes.append(self.required_css_class)
        return render_to_string(
            self.template_name,
            {
                "field": self.field,
                "widget_then_label": isinstance(
                    self.field.field.widget, forms.CheckboxInput
                ),
                "label_tag": self.field.label_tag(
                    label_suffix=self.label_suffix,
                    attrs=(
                        {"class": " ".join(extra_classes)} if extra_classes else None
                    ),
                ),
                "css_classes": self.field.css_classes(
                    extra_classes=extra_classes
                    + [f"widget--{self.field.field.widget.__class__.__name__.lower()}"]
                ),
            },
        )


class PlainFieldWrapper(FieldWrapper):
    template_name = "fineforms/field-plain.html"


@html_safe
class FieldsWrapper:
    template_name = "fineforms/fields.html"

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields

    def __str__(self):
        bfs = [self.form[field] for field in self.fields]
        return render_to_string(
            self.template_name,
            {
                "form": self.form,
                "fields": [wrapper("field")(bf) for bf in bfs if not bf.is_hidden],
                "hidden": mark_safe("".join(str(bf) for bf in bfs if bf.is_hidden)),
            },
        )


FINEFORMS_WRAPPERS = {
    "errors": ErrorsWrapper,
    "field": FieldWrapper,
    "field-plain": PlainFieldWrapper,
    "fields": FieldsWrapper,
}


@cache
def wrapper(type):
    typ = (FINEFORMS_WRAPPERS | getattr(settings, "FINEFORMS_WRAPPERS", {}))[type]
    return import_string(typ) if isinstance(typ, str) else typ
