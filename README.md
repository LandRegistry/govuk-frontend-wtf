# GOV.UK Frontend WTForms Widgets

[![PyPI version](https://badge.fury.io/py/govuk-frontend-wtf.svg)](https://pypi.org/project/govuk-frontend-wtf/)
![govuk-frontend 3.14.0](https://img.shields.io/badge/govuk--frontend%20version-3.14.0-005EA5?logo=gov.uk&style=flat)
[![Python package](https://github.com/LandRegistry/govuk-frontend-wtf/actions/workflows/python-package.yml/badge.svg)](https://github.com/LandRegistry/govuk-frontend-wtf/actions/workflows/python-package.yml)

**GOV.UK Frontend WTForms is a [community tool](https://design-system.service.gov.uk/community/resources-and-tools/) of the [GOV.UK Design System](https://design-system.service.gov.uk/). The Design System team is not responsible for it and cannot support you with using it. Contact the [maintainers](#contributors) directly if you need [help](#support) or you want to request a feature.**

This repository contains a set of [WTForms widgets](https://wtforms.readthedocs.io/en/2.3.x/widgets/) used to render [WTForm fields](https://wtforms.readthedocs.io/en/2.3.x/fields/) using [GOV.UK Frontend](https://design-system.service.gov.uk/) component styling. This is done using Jinja macros from the [GOV.UK Frontend Jinja](https://github.com/LandRegistry/govuk-frontend-jinja) port of the original GOV.UK Frontend Nunjucks macros. These are kept up-to-date with GOV.UK Frontend releases, are thoroughly tested and produce 100% equivalent markup.

This approach also renders the associated error messages in the appropriate place, shows the error summary component at the top of the page and sets all related accessibility ARIA attributes. Adding the appropriate [widget](#widgets) to your existing form Python class, along with far simpler templates, makes it quick and easy to produce fully GOV.UK compliant forms.

- Package: [https://pypi.org/project/govuk-frontend-wtf/](https://pypi.org/project/govuk-frontend-wtf/)
- Demo app: [https://github.com/LandRegistry/govuk-frontend-wtf-demo](https://github.com/LandRegistry/govuk-frontend-wtf-demo)
- Live demo: [https://govuk-frontend-wtforms.herokuapp.com/](https://govuk-frontend-wtforms.herokuapp.com/)

## How to use

For more detailed examples please refer to the [demo app source code](https://github.com/LandRegistry/govuk-frontend-wtf-demo).

After running `pip install govuk-frontend-wtf`, ensure that you tell Jinja where to load the templates from using the `PackageLoader`, register `WTFormsHelpers`, then set an environment variable for `SECRET_KEY`.

`app/__init__.py`:

```python
from flask import Flask
from govuk_frontend_wtf.main import WTFormsHelpers
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

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

Import and include the relevant widget on each field in your form class (see [table below](#widgets)). Note that in this example `widget=GovTextInput()` is the only difference relative to a standard Flask-WTF form definition.

`app/forms.py`:

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

Create a route to serve your form and template.

`app/routes.py`:

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

Finally, in your template set the page title appropriately if there are any form validation errors, as per [GOV.UK Design System guidance](https://design-system.service.gov.uk/components/error-summary/#how-it-works). Include the `govukErrorSummary()` component at the start of the `content` block. Pass parameters in a dictionary to your form field as per the associated [component macro options](https://design-system.service.gov.uk/components/).

`app/templates/example_form.html`:

```html
{% extends "base.html" %}

{%- from 'govuk_frontend_jinja/components/error-summary/macro.html' import govukErrorSummary -%}

{% block pageTitle %}{%- if form and form.errors %}Error: {% endif -%}Example form – GOV.UK Frontend WTForms Demo{% endblock %}

{% block content %}
<div class="govuk-grid-row">
    <div class="govuk-grid-column-two-thirds">
        {% if form.errors %}
            {{ govukErrorSummary(wtforms_errors(form)) }}
        {% endif %}

        <h1 class="govuk-heading-xl">Example form</h1>

        <form action="" method="post" novalidate>
            {{ form.csrf_token }}
            
            {{ form.email_address(params={
              'type': 'email',
              'autocomplete': 'email',
              'spellcheck': false
            }) }}
            
            {{ form.submit }}
        </form>
    </div>
</div>
{% endblock %}
```

## Widgets

The available widgets and their corresponding Flask-WTF field types are as follows:

| WTForms Field                                                                                             | GOV.​UK Widget(s)               | Notes |
| --------------------------------------------------------------------------------------------------------- | ------------------------------ | ----- |
| [BooleanField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.BooleanField)               | GovCheckboxInput               |       |
| [DateField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DateField)                     | GovDateInput                   |       |
| [DateTimeField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DateTimeField)             | GovDateInput                   |       |
| [DecimalField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DecimalField)               | GovTextInput                   |       |
| [FileField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.FileField)                     | GovFileInput                   |       |
| [MultipleFileField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.MultipleFileField)     | GovFileInput(multiple=True)    | Note that you need to specify `multiple=True` when invoking the widget in your form class. _Not_ when you render it in the Jinja template. |
| [FloatField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.FloatField)                   | GovTextInput                   |       |
| [IntegerField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.IntegerField)               | GovTextInput                   | Use `params` to specify a `type` if you need to use HTML5 number elements. This will not happen automatically. |
| [PasswordField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.PasswordField)             | GovPasswordInput               |       |
| [RadioField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.RadioField)                   | GovRadioInput                  |       |
| [SelectField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectField)                 | GovSelect                      |       |
| [SelectMultipleField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectMultipleField) | GovCheckboxesInput             | Note that this renders checkboxes as `<select multiple>` elements are frowned upon. |
| [SubmitField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SubmitField)                 | GovSubmitInput                 |       |
| [StringField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.StringField)                 | GovTextInput                   |       |
| [TextAreaField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.TextAreaField)             | GovTextArea, GovCharacterCount |       |

In order to generate things like email fields using `GovTextInput` you will need to pass additional params through when rendering it as follows:

```html
{{ form.email_address(params={'type': 'email', 'autocomplete': 'email', 'spellcheck': false}) }}
```

## Running the tests

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r tests/requirements.txt
pytest --cov=govuk_frontend_wtf --cov-report=term-missing --cov-branch
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/LandRegistry/govuk-frontend-wtf/tags).

## How to contribute

We welcome contribution from the community. If you want to contribute to this project, please review the [code of conduct](CODE_OF_CONDUCT.md) and [contribution guidelines](CONTRIBUTING.md).

## Contributors

- [Matt Shaw](https://github.com/matthew-shaw) (Primary maintainer)
- [Andy Mantell](https://github.com/andymantell) (Original author)
- [Hugo Baldwin](https://github.com/byzantime)
- [Dale Potter](https://github.com/dalepotter)
- [Gabriel Ionescu](https://github.com/ionescuig)
- [Matt Pease](https://github.com/Skablam)

## Support

This software is provided _"as-is"_ without warranty. Support is provided on a _"best endeavours"_ basis by the maintainers and open source community.

If you are a civil servant you can sign up to the [UK Government Digital Slack](https://ukgovernmentdigital.slack.com/signup) workspace to contact the maintainers listed [above](#contributors) and the community of people using this project in the [#govuk-design-system](https://ukgovernmentdigital.slack.com/archives/C6DMEH5R6) channel.

Otherwise, please see the [contribution guidelines](CONTRIBUTING.md) for how to raise a bug report or feature request.
