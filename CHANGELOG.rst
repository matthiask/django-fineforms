==========
Change log
==========

`Next version`_
===============

- Added CSS classes to the default ``ff_errors`` template's top level
  element and also to the error list.


`0.3`_ (2017-09-04)
===================

- Django also adds ``required_css_class`` to the label tag; do the same
  (and also add ``error`` because it simplifies the code).
- Parametrize the CSS classes used for ``error_css_class`` and
  ``required_css_class``.
- Add an additional wrapping ``div`` to the default
  ``widget_then_label`` field template to avoid flex children layout.
- Add the widget class name as a ``widget--$name`` CSS class to the
  output. This makes styling radio selects more straightforward (use
  a ``.widget--radioselect ...`` CSS selector)


`0.2`_ (2017-05-25)
===================

- Documentation work.
- Allow specifying additional wrappers as dotted Python paths to avoid
  problems with circular imports.
- The ``FieldWrapper`` now passes ``label_tag`` and ``css_classes`` into
  the template; ``label_tag`` uses ``FieldWrapper.label_suffix``
  (defaulting to ``''``), and ``css_classes`` contains ``required`` and
  ``error`` if fitting and if ``Form.required_css_class`` and
  ``Form.error_css_class`` are undefined.


`0.1`_ (2017-05-16)
===================

- Initial public version.

.. _0.1: https://github.com/matthiask/django-fineforms/commit/06f30791f3d
.. _0.2: https://github.com/matthiask/django-fineforms/compare/0.1...0.2
.. _0.3: https://github.com/matthiask/django-fineforms/compare/0.2...0.3
.. _Next version: https://github.com/matthiask/django-fineforms/compare/0.3...master
