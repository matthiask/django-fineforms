==========
Change log
==========

`Next version`_
===============

- Modernized the package, added Python 3.11, 3.12 and Django 5.1.

.. _Next version: https://github.com/matthiask/django-fineforms/compare/0.7...main


`0.7`_ (2023-04-13)
===================

.. _0.7: https://github.com/matthiask/django-fineforms/compare/0.6...0.7

- Dropped support for Python < 3.8, Django < 3.2.
- Added Django 4.1 and 4.2.
- Added Romansh translations.


`0.6`_ (2021-02-16)
===================

- Added ``forms`` to the context of ``fineforms/errors.html``, ``form`` to the
  context of ``fineforms/fields.html``.
- Switched from Travis CI to GitHub actions.


`0.5`_ (2019-02-13)
===================

- Added a ``ff_submit`` tag for showing submit buttons.
- All defaults are arbitrary. Arbitrarily changed the default for the
  ``foundation_xy_grid`` package to only show fields and labels in one
  line for large screend.


`0.4`_ (2018-12-26)
===================

- Added CSS classes to the default ``ff_errors`` template's top level
  element and also to the error list.
- Moved all wrappers into ``fineforms.wrappers``.
- Reformatted the code using black.
- Modified template tags to pass on keyword arguments to the wrappers
  they instantiate.
- Added a template package using `Foundation's XY-grid
  <https://foundation.zurb.com/sites/docs/xy-grid.html>`__, usable by
  adding ``fineforms.pacakges.foundation_xy_grid`` before ``fineforms``
  to ``INSTALLED_APPS``.


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
.. _0.4: https://github.com/matthiask/django-fineforms/compare/0.3...0.4
.. _0.5: https://github.com/matthiask/django-fineforms/compare/0.4...0.5
.. _0.6: https://github.com/matthiask/django-fineforms/compare/0.5...0.6
.. _Next version: https://github.com/matthiask/django-fineforms/compare/0.6...main
