from wtforms.widgets.core import FileInput, Input, PasswordInput, Select, SubmitInput, TextArea, TextInput

from govuk_frontend_wtf.gov_form_base import GovFormBase, GovIterableBase

"""Lifted from WTForms and modified to generate GOV.UK markup

The upstream code should be monitored when updating WTForms to
see if any modifications need to be brought in
"""


class GovInput(GovFormBase, Input):
    """Render a basic ``<input>`` field.

    This is used as the basis for most of the other input fields.

    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    template = "govuk_frontend_wtf/input.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        return super().__call__(field, **kwargs)


class GovTextInput(GovInput, TextInput):
    """Render a single-line text input."""

    input_type = "text"


class GovPasswordInput(GovInput, PasswordInput):
    """Render a password input.

    For security purposes, this field will not reproduce the value on a form
    submit by default. To have the value filled in, set `hide_value` to
    `False`.
    """

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs["value"] = ""
        return super().__call__(field, **kwargs)


class GovCheckboxesInput(GovIterableBase):
    """Multiple checkboxes, from a SelectMultipleField

    This widget type doesn't exist in WTForms - the recommendation
    there is to use a combination of the list and checkbox widgets.
    However in the GOV.UK macros this type of field is not simply
    a list of smaller widgets - multiple checkboxes are a single
    construct of their own.
    """

    template = "govuk_frontend_wtf/checkboxes.html"
    input_type = "checkbox"

    def map_gov_params(self, field, **kwargs):
        params = super().map_gov_params(field, **kwargs)
        params.setdefault(
            "fieldset",
            {
                "legend": {
                    "text": field.label.text,
                },
            },
        )
        return params


class GovCheckboxInput(GovCheckboxesInput):
    """Render a single checkbox (i.e. a WTForms BooleanField)."""

    def __call__(self, field, **kwargs):
        # We are subclassing GovCheckboxesInput which expects
        # the field to be an iterable yielding each checkbox "subfield"
        # In order to make our single BooleanField comply with this, we
        # need to provide it with a similar construct, but which only
        # yields a single checkbox
        class IterableField(object):
            def __init__(self, field):
                self.field = field
                self.max = 1

            def __iter__(self):
                self.index = 0
                return self

            def __next__(self):
                if self.index < self.max:
                    self.index += 1

                    return self.field
                else:
                    raise StopIteration

            def __getattr__(self, name):
                return getattr(self.field, name)

        field_group = IterableField(field)

        return super().__call__(field_group, **kwargs)

    def map_gov_params(self, field, **kwargs):
        params = super().map_gov_params(field, **kwargs)
        params.pop("fieldset")
        return params


class GovRadioInput(GovIterableBase):
    """Render radio button inputs.

    Uses the field label as the fieldset legend.
    """

    template = "govuk_frontend_wtf/radios.html"
    input_type = "radio"

    def map_gov_params(self, field, **kwargs):
        params = super().map_gov_params(field, **kwargs)
        params.setdefault(
            "fieldset",
            {
                "legend": {"text": field.label.text},
            },
        )
        return params


class GovDateInput(GovFormBase):
    """Renders three input fields representing Day, Month and Year.

    To be used as a widget for WTForms' DateField or DateTimeField.
    The input field labels are hardcoded to "Day", "Month" and "Year".
    The provided label is set as a legend above the input fields.
    The field names MUST all be the same for this widget to work.
    """

    template = "govuk_frontend_wtf/date.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return super().__call__(field, **kwargs)

    def map_gov_params(self, field, **kwargs):
        params = super().map_gov_params(field, **kwargs)
        day, month, year = [None] * 3
        if field.raw_data is not None:
            day, month, year = field.raw_data
        elif field.data:
            day, month, year = field.data.strftime("%d %m %Y").split(" ")

        params.setdefault(
            "fieldset",
            {
                "legend": {"text": field.label.text},
            },
        )
        params.setdefault(
            "items",
            [
                {
                    "label": "Day",
                    "id": "{}-day".format(field.name),
                    "name": field.name,
                    "classes": " ".join(
                        [
                            "govuk-input--width-2",
                            "govuk-input--error" if field.errors else "",
                        ]
                    ).strip(),
                    "value": day,
                },
                {
                    "label": "Month",
                    "id": "{}-month".format(field.name),
                    "name": field.name,
                    "classes": " ".join(
                        [
                            "govuk-input--width-2",
                            "govuk-input--error" if field.errors else "",
                        ]
                    ).strip(),
                    "value": month,
                },
                {
                    "label": "Year",
                    "id": "{}-year".format(field.name),
                    "name": field.name,
                    "classes": " ".join(
                        [
                            "govuk-input--width-4",
                            "govuk-input--error" if field.errors else "",
                        ]
                    ).strip(),
                    "value": year,
                },
            ],
        )
        return params


class GovFileInput(GovInput, FileInput):
    """Render a file chooser input.

    :param multiple: allow choosing multiple files
    """

    template = "govuk_frontend_wtf/file-upload.html"

    def __call__(self, field, **kwargs):
        # browser ignores value of file input for security
        kwargs["value"] = False

        if self.multiple:
            kwargs["multiple"] = True

        return super().__call__(field, **kwargs)


class GovSubmitInput(GovInput, SubmitInput):
    """Renders a submit button.

    The field's label is used as the text of the submit button instead of the
    data on the field.
    """

    template = "govuk_frontend_wtf/button.html"

    def __call__(self, field, **kwargs):
        return super().__call__(field, **kwargs)

    def map_gov_params(self, field, **kwargs):
        params = super().map_gov_params(field, **kwargs)

        params.setdefault("text", field.label.text)
        params.setdefault("element", "button")

        return params


class GovTextArea(GovFormBase, TextArea):
    """Renders a multi-line text area.

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    template = "govuk_frontend_wtf/textarea.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return super().__call__(field, **kwargs)


class GovCharacterCount(GovFormBase, TextArea):
    """Renders a multi-line text area with a character count.

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    template = "govuk_frontend_wtf/charactercount.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return super().__call__(field, **kwargs)


class GovSelect(GovFormBase, Select):
    """Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """

    template = "govuk_frontend_wtf/select.html"

    def __call__(self, field, **kwargs):
        if self.multiple:
            raise Exception(
                "Please do not render mutliselect elements as a select box"
                " - you should use checkboxes instead in order to comply with"
                " the GOV.UK service manual"
            )

        kwargs.setdefault("id", field.id)

        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        kwargs["items"] = []

        # Construct select box choices
        for val, label, selected in field.iter_choices():
            item = {"text": label, "value": val, "selected": selected}

            kwargs["items"].append(item)

        return super().__call__(field, **kwargs)

    def map_gov_params(self, field, **kwargs):

        params = super().map_gov_params(field, **kwargs)

        params["items"] = kwargs["items"]

        return params
