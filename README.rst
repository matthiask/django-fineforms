============================================
django-fineforms - Form rendering for Django
============================================

.. image:: https://travis-ci.org/matthiask/django-fineforms.png?branch=master
   :target: https://travis-ci.org/matthiask/django-fineforms

This library offers an improved replacement for Django's own form
rendering methods (``as_p``, ``as_table`` etc.) while staying simple
and extensible but without introducing a whole new framework.

django-fineforms consists of a template tag library and a few
opinionated default templates.


Goals
=====

- Stay simple and extensible
- Avoid options, settings and customizability as much as possible


Non-goals
=========

- Compete with django-crispy-forms or any of the more flexible libraries
  out there


Installation
============

Simply ``pip install django-fineforms``, and add ``fineforms`` to your
``INSTALLED_APPS``.


High-level overview
===================

The template tags mostly wrap their arguments in wrapper classes that do
the real work. For example, ``{% ff_field %}`` simply wraps the passed
field in a wrapper defined in the ``FINEFORMS_WRAPPERS`` setting. All
wrappers use a template to render their output. The default wrapper
types are as follows::

    {
        'errors': ErrorsWrapper,
        'field': FieldWrapper,
        'field-plain': PlainFieldWrapper,
        'fields': FieldsWrapper,
    }

The wrappers themselves mostly aren't configurable, but you can replace
individual wrappers (or all of them) by adding a ``FINEFORMS_WRAPPERS``
setting. You do not have to override all of them; if you only want to
add another wrapper for a specific field type you could just set::

    FINEFORMS_WRAPPERS = {
        'specific': 'app.wrappers.SpecificWrapper',
    }

... and use this wrapper as ``{% ff_field some_field type='specific' %}``
somewhere in your templates.


Template tags
=============

All template tags are contained in the ``fineforms`` library.

``{% ff_field field [type=field] %}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template: ``fineforms/field.html``

Render a single field. The wrapper can be optionally overridden by
passing a different type. The key has to exist in the
``FINEFORMS_WRAPPERS`` dictionary.

The default implementation renders the label, the widget, help text and
errors related to the field. It is recommended to also set the
``error_css_class`` and ``required_css_class`` form attributes; those
classes are also added to the output.

The ``field-plain`` type can be used if the widget should be rendered
alone. A wrapping ``<span>`` tag still contains the CSS classes
mentioned above.


``{% ff_fields form [fields='a,b,c' | exclude='a,b,c'] %}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template: ``fineforms/fields.html``

Render fields of a form. ``fields`` and ``exclude`` are
comma-separated strings that can be used to only render a selection of
fields. The ``fields`` parameter takes precedence if both are given.

Hidden fields are rendered separately at the end, all other fields are
wrapped using ``FINEFORMS_WRAPPERS['field']`` and rendered as well.


``{% ff_errors form1 [form2 ...] %}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template: ``fineforms/errors.html``

Render form errors at the top. The default implementation renders all
non-field errors, and all errors from hidden fields.  Falsy parameters
(i.e. ``None``) are filtered out for you. If there aren't any errors at
all nothing is rendered.


``{% ff_hidden_fields form1 [form2 ...] %}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This template tag is the outlier in that it does not use a template at
all. The return value is the concatenated result of rendering all hidden
fields of all passed forms. Falsy parameters (i.e. ``None``) are
filtered out for you.

Please note that ``{% ff_fields %}`` adds hidden fields to the output
automatically.
