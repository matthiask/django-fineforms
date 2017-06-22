from django import forms
from django.template import Context, Template
from django.test import TestCase


class Form(forms.Form):
    email = forms.EmailField()
    optional = forms.CharField(required=False)
    hidden = forms.CharField(widget=forms.HiddenInput)


class TagsTestCase(TestCase):
    maxDiff = None

    def test_field(self):
        t = Template('{% load fineforms %}{% ff_field form.email %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
<div class="required row">
  <div class="small-12 medium-3 columns">
    <label class="required" for="id_email">Email</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="email" name="email" required id="id_email" />
  </div>
</div>
''')

    def test_fields(self):
        t = Template('{% load fineforms %}{% ff_fields form %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
<div class="required row">
  <div class="small-12 medium-3 columns">
    <label class="required" for="id_email">Email</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="email" name="email" required id="id_email" />
  </div>
</div><div class=" row">
  <div class="small-12 medium-3 columns">
    <label for="id_optional">Optional</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="text" name="optional" id="id_optional" />
  </div>
</div><input id="id_hidden" name="hidden" type="hidden" />
''')

        t = Template(
            '{% load fineforms %}{% ff_fields form fields="email" %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
<div class="required row">
  <div class="small-12 medium-3 columns">
    <label class="required" for="id_email">Email</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="email" name="email" required id="id_email" />
  </div>
</div>
''')

        t = Template(
            '{% load fineforms %}'
            '{% ff_fields form exclude="optional,email" %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
<input id="id_hidden" name="hidden" type="hidden" />
''')

        # Test that fields has precedence over exclude
        t = Template(
            '{% load fineforms %}'
            '{% ff_fields form fields="hidden" exclude="email,hidden" %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
<input id="id_hidden" name="hidden" type="hidden" />
''')

    def test_errors(self):
        t = Template(
            '{% load fineforms %}'
            '{% ff_errors form nothing %}'
            '{% ff_fields form %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form({}),
            })),
            '''\
<div class="row">
  <div class="small-12 columns">
    <h3>Please correct the following errors:</h3>
      <ul>
        <li>(Hidden field hidden) This field is required.</li>
      </ul>
  </div>
</div>
<div class="row error required">
  <div class="small-12 medium-3 columns">
    <label class="error required" for="id_email">Email</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="email" name="email" id="id_email" required />
    <ul class="errorlist"><li>This field is required.</li></ul>
  </div>
</div>
<div class="row ">
  <div class="small-12 medium-3 columns">
    <label for="id_optional">Optional</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="text" name="optional" id="id_optional" />
  </div>
</div>
<input type="hidden" name="hidden" id="id_hidden" />
''')

    def test_valid_form(self):
        t = Template('{% load fineforms %}{% ff_errors form nothing %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form({'email': 'test@example.com', 'hidden': 'yes'}),
            })),
            '',
        )

    def test_hidden_fields(self):
        t = Template('{% load fineforms %}{% ff_hidden_fields form nothing %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '<input id="id_hidden" name="hidden" type="hidden" />',
        )

    def test_additional(self):
        t = Template(
            '{% load fineforms %}{% ff_field form.email type="additional" %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
ADDITIONAL<div class="required row">
<div class="columns medium-3 small-12">
<label class="required" for="id_email">
Email
</label>
</div><div class="columns medium-9 small-12">
<input id="id_email" name="email" required type="email" />
</div>
</div>
''')
