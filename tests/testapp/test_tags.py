from django import forms
from django.test import TestCase
from django.template import Context, Template


class Form(forms.Form):
    email = forms.EmailField()
    hidden = forms.CharField(widget=forms.HiddenInput)


class TagsTestCase(TestCase):
    def test_field(self):
        t = Template('{% load fineforms %}{% ff_field form.email %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form(),
            })),
            '''\
<div class=" row">
  <div class="small-12 medium-3 columns">
    <label for="id_email">Email:</label>
  </div>
  <div class="small-12 medium-9 columns">
    <input type="email" name="email" required id="id_email" />
  </div>
</div>
''')

    def test_errors(self):
        t = Template('{% load fineforms %}{% ff_errors form nothing %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form({}),
            })),
            '''\
<div class="row">
  <div class="small-12 columns">
    <h3>
    Please correct the following errors:
    </h3>
    <ul>
    <li>
    (Hidden field hidden) This field is required.
    </li>
    </ul>
  </div>
</div>
''')

    def test_valid_form(self):
        t = Template('{% load fineforms %}{% ff_errors form nothing %}')
        self.assertHTMLEqual(
            t.render(Context({
                'form': Form({'email': 'test@example.com', 'hidden': 'yes'}),
            })),
            '',
        )
