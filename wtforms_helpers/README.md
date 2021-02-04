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
