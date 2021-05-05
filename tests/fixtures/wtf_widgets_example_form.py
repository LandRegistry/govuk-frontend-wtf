from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovCheckboxesInput,
    GovCheckboxInput,
    GovDateInput,
    GovFileInput,
    GovPasswordInput,
    GovRadioInput,
    GovSelect,
    GovSubmitInput,
    GovTextArea,
    GovTextInput,
)
from wtforms.fields import (
    BooleanField,
    DateField,
    DecimalField,
    FileField,
    FloatField,
    IntegerField,
    MultipleFileField,
    PasswordField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Email, EqualTo, InputRequired, ValidationError


class ExampleForm(FlaskForm):
    string_field = StringField(
        "StringField",
        widget=GovTextInput(),
        validators=[InputRequired(message="StringField is required")],
    )

    date_field = DateField(
        "DateField",
        format="%d %m %Y",
        widget=GovDateInput(),
        validators=[InputRequired(message="Date is required")]
    )

    email_field = StringField(
        "Email address",
        widget=GovTextInput(),
        validators=[InputRequired(message="Email address is required"), Email()],
    )

    float_field = FloatField(
        "FloatField",
        widget=GovTextInput(),
        validators=[InputRequired(message="FloatField is required")],
    )

    integer_field = IntegerField(
        "IntegerField",
        widget=GovTextInput(),
        validators=[InputRequired(message="IntegerField is required")],
    )

    decimal_field = DecimalField(
        "DecimalField",
        widget=GovTextInput(),
        validators=[InputRequired(message="DecimalField is required")],
    )

    textarea_field = TextAreaField(
        "TextAreaField",
        widget=GovTextArea(),
        validators=[InputRequired(message="TextAreaField is required")],
    )

    boolean_field = BooleanField(
        "BooleanField",
        widget=GovCheckboxInput(),
        validators=[InputRequired(message="Please tick the box")],
    )

    select_field = SelectField(
        "SelectField",
        widget=GovSelect(),
        validators=[InputRequired(message="Please select an option")],
        choices=[
            ("", "Please select"),
            ("one", "One"),
            ("two", "Two"),
            ("three", "Three"),
        ],
        default="",
    )

    select_multiple_field = SelectMultipleField(
        "SelectMultipleField",
        widget=GovCheckboxesInput(),
        validators=[InputRequired(message="Please select an option")],
        choices=[("one", "One"), ("two", "Two"), ("three", "Three")],
    )

    radio_field = RadioField(
        "RadioField",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Please select an option")],
        choices=[("one", "One"), ("two", "Two"), ("three", "Three")],
    )

    file_field = FileField(
        "FileField",
        widget=GovFileInput(),
        validators=[InputRequired(message="Please upload a file")],
    )

    multiple_file_field = MultipleFileField(
        "MultipleFileField",
        widget=GovFileInput(multiple=True),
        validators=[InputRequired(message="Please upload a file")],
    )

    password_field = PasswordField(
        "PasswordField",
        widget=GovPasswordInput(),
        validators=[
            InputRequired("Password is required"),
            EqualTo(
                "password_retype_field",
                message="Please ensure both password fields match",
            ),
        ],
    )

    password_retype_field = PasswordField(
        "Re-type your password",
        widget=GovPasswordInput(),
        validators=[InputRequired("Please retype your password")],
    )

    submit_button = SubmitField("SubmitField", widget=GovSubmitInput())

    def validate_string_field(self, field):
        if field.data != "John Smith":
            raise ValidationError('Example serverside error - type "John Smith" into this field to suppress it')
