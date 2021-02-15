# GOV.UK Frontend WTForms Widgets

[![PyPI version](https://badge.fury.io/py/govuk-frontend-wtf.svg)](https://pypi.org/project/govuk-frontend-wtf/)
![govuk-frontend 3.11.0](https://img.shields.io/badge/govuk--frontend%20version-3.11.0-005EA5?logo=gov.uk&style=flat)
![Build](https://github.com/LandRegistry/govuk-frontend-wtf/workflows/Build/badge.svg)

[TODO] One paragraph overview...

- Package: [https://pypi.org/project/govuk-frontend-wtf/](https://pypi.org/project/govuk-frontend-wtf/)
- Demo app: [https://github.com/LandRegistry/govuk-frontend-wtf-demo](https://github.com/LandRegistry/govuk-frontend-wtf-demo)
- Live demo: [https://govuk-frontend-wtf.herokuapp.com/](https://govuk-frontend-wtf.herokuapp.com/)

## How to use

For a more detailed demo please refer to the [demo app](https://github.com/LandRegistry/govuk-frontend-wtf-demo) source code.

After running `pip install govuk-frontend-wtf`, ensure that you tell Jinja where to load the templates from using the `PackageLoader` and register `WTFormsHelpers` as follows:

```python
from flask import Flask
from govuk_frontend_wtf.main import WTFormsHelpers
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

app = Flask(__name__)

app.jinja_loader = ChoiceLoader(
    [
        PackageLoader("app"),
        PrefixLoader(
            {
                "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                "govuk_frontend_wtf": PackageLoader("govuk_frontend_wtf"),
            }
        ),
    ]
)

WTFormsHelpers(app)
```

Import and include the relevant widget on each field in your form class (see table below).

```python
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovSubmitInput, GovTextInput
from wtforms import StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


class ExampleForm(FlaskForm):
    email_address = StringField(
        "Email address",
        widget=GovTextInput(),
        validators=[
            InputRequired(message="Enter an email address"),
            Length(max=256, message="Email address must be 256 characters or fewer"),
            Email(message="Enter an email address in the correct format, like name@example.com"),
        ],
        description="We’ll only use this to send you a receipt",
    )

    submit = SubmitField("Continue", widget=GovSubmitInput())
```

In your template make sure to set the page title appropriately if there are any form validation errors. Also include the `govukErrorSummary()` component at the start of the `content` block. You can pass additional parameters or attributes to your form field as per the associated macro's parameters.

```html
{% extends "base.html" %}

{%- from 'govuk_frontend_jinja/components/back-link/macro.html' import govukBackLink -%}
{%- from 'govuk_frontend_jinja/components/error-summary/macro.html' import govukErrorSummary -%}

{% block pageTitle %}{%- if form and form.errors %}Error: {% endif -%}Example form – GOV.UK Frontend WTForms Demo{% endblock %}

{% block beforeContent %}
  {{ govukBackLink({
    'text': "Back",
    'href': url_for('index')
  }) }}
{% endblock %}

{% block content %}
{% if form.errors %}
    {{ govukErrorSummary(wtforms_errors(form)) }}
{% endif %}

<h1 class="govuk-heading-l">Example form</h1>
<div class="govuk-grid-row">
    <div class="govuk-grid-column-two-thirds">
        <form action="" method="post" novalidate>
            {{form.csrf_token}}
            
            {{form.email_address(params={
              'hint': {
                'text': form.email_address.description
              }
            }, type="email", spellcheck="false", autocomplete="email")}}
            
            {{form.submit}}
        </form>
    </div>
</div>
{% endblock %}
```

Finally, create a route to serve your form and template.

```python
from flask import redirect, render_template, url_for

from app import app
from app.forms import ExampleForm

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/example-form", methods=["GET", "POST"])
def example():
    form = ExampleForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("example_form.html", form=form)
```

## Running the tests

[TODO]

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/LandRegistry/govuk-frontend-wtf/tags).

## Contributors

- [Matt Shaw](https://github.com/matthew-shaw) (Primary maintainer)
- [Andy Mantell](https://github.com/andymantell) (Original author)
- [Hugo Baldwin](https://github.com/byzantime)


--- Previous README below ---

# Flask-WTF forms (And GOV.​UK flavoured widgets)

[Flask-WTF](https://flask-wtf.readthedocs.io/) is used for building HTML forms, making things like form validation and rendering of errors much easier than having to build this yourself. The [Flask-WTF documentation](https://flask-wtf.readthedocs.io/) covers the standard use cases and you should refer to this.

In addition to the standard use case however, flask-skeleton-ui includes custom widgets that can be used to render Flask-WTF forms in the GOV.​UK style. These widgets automatically render error messages in the appropriate places as well as showing an error summary at the top of the page in a fully GOV.​UK compliant manner.

## Defining a GOV.​UK style form

In order to use the GOV.​UK style widgets, when you create your form class, you should specify the appropriate widget as follows:

_(Excerpt from [unit_tests/fixtures/wtf_macros_example_form.py](unit_tests/fixtures/wtf_macros_example_form.py)_
```
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired
from flask_skeleton_ui.custom_extensions.wtforms_helpers.wtforms_widgets import GovTextInput


class ExampleForm(FlaskForm):
    string_field = StringField('StringField',
                               widget=GovTextInput(),
                               validators=[InputRequired(message='StringField is required')],
                               )
```

Note the `widget=GovTextInput()` line. This is the only difference relative to a standard Flask-WTF form definition.

This is then rendered in your jinja templates as follows which is completely standard Flask-WTF code:

```
{{ form['string_field'] }}
```

Where this then deviates from Flask-WTF is the ability to pass additional parameters to the underlying GOV.​UK jinja macros. For example:



```
{{ form['string_field'](params={
  'hint': {
    'text': 'This is a hint'
  }
}) }}
```

By passing a dict in via the `params` argument, this will be passed along to the underlying GOV.​UK macro in order to customize the output. More information about these params can be found in the [design system](https://design-system.service.gov.uk/) or if it suits you better, by [reading the source code of the templates themselves](https://github.com/alphagov/govuk-frontend/tree/master/src/components) (Highly recommended as this will always be the most authoritative).

The available widgets and their corresponding Flask-WTF field types are as follows:

| WTForms field type<br><small>wtforms.fields.[TYPE]</small> | GOV.​UK styled widget<br><small>flask_skeleton_ui.custom_extensions.wtforms_helpers.wtforms_widgets.[WIDGET]</small> | Notes |
| -------------------- | --------------------------- | ---------- |
| StringField          | GovTextInput                |            |
| FloatField           | GovTextInput                |            |
| IntegerField         | GovTextInput                | Use `params` to specify a `type` if you need to use html5 number elements. This will not happen automatically. |
| DecimalField         | GovTextInput                |            |
| TextAreaField        | GovTextArea                 |            |
| BooleanField         | GovCheckboxInput            |            |
| SelectField          | GovSelect                   |            |
| SelectMultipleField  | GovCheckboxesInput          | Note that this renders checkboxes as `<select multiple>` elements are frowned upon |
| RadioField           | GovRadioInput               |            |
| FileField            | GovFileInput                |            |
| MultipleFileField    | GovFileInput(multiple=True) | Note that you need to specify `multiple=True` when invoking the widget in your form class. _Not_ when you render it in the jinja. |
| PasswordField        | GovPasswordInput            |            |
| SubmitField          | GovSubmitInput              |            |


In order to generate things like email fields using `GovTextInput` you will need to pass additional params through when rendering it as follows:

```
{{ form['email_field'](params={'type': 'email'}) }}
```

An example of this can be found in [unit_tests/fixtures/wtf_macros_example_form.py](unit_tests/fixtures/wtf_macros_example_form.py) which is a full FlaskForm setup in order to run the unit tests but is also useful as a reference.

## Errors

When validation errors occur, they will automatically be rendered next to the appropriate form field.

In addition to this, the base layout.html template includes code which will render the error summary in the correct place at the top of the page, as well as prefixing the page title with "Error:" as per the GOV.​UK recomendation.
