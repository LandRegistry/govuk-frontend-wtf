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
from wtforms import Form as NoCsrfForm
from wtforms.fields import (
    BooleanField,
    DateField,
    DecimalField,
    FieldList,
    FileField,
    FloatField,
    FormField,
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


class ExampleChildForm(NoCsrfForm):
    string_field = StringField(
        "StringField",
        widget=GovTextInput(),
        validators=[InputRequired(message="StringField is required")],
    )


class ExampleForm(FlaskForm):
    string_field = StringField(
        "StringField",
        widget=GovTextInput(),
        validators=[InputRequired(message="StringField is required")],
        description="StringFieldHint",
    )

    date_field = DateField(
        "DateField",
        format="%d %m %Y",
        widget=GovDateInput(),
        validators=[InputRequired(message="Date is required")],
        description="DateFieldHint",
    )

    email_field = StringField(
        "EmailField",
        widget=GovTextInput(),
        validators=[InputRequired(message="EmailField is required"), Email()],
        description="EmailFieldHint",
    )

    float_field = FloatField(
        "FloatField",
        widget=GovTextInput(),
        validators=[InputRequired(message="FloatField is required")],
        description="FloatFieldHint",
    )

    integer_field = IntegerField(
        "IntegerField",
        widget=GovTextInput(),
        validators=[InputRequired(message="IntegerField is required")],
        description="IntegerFieldHint",
    )

    decimal_field = DecimalField(
        "DecimalField",
        widget=GovTextInput(),
        validators=[InputRequired(message="DecimalField is required")],
        description="DecimalFieldHint",
    )

    textarea_field = TextAreaField(
        "TextAreaField",
        widget=GovTextArea(),
        validators=[InputRequired(message="TextAreaField is required")],
        description="TextAreaFieldHint",
    )

    boolean_field = BooleanField(
        "BooleanField",
        widget=GovCheckboxInput(),
        validators=[InputRequired(message="Please tick the box")],
        description="BooleanFieldHint",
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
        description="SelectFieldHint",
    )

    select_multiple_field = SelectMultipleField(
        "SelectMultipleField",
        widget=GovCheckboxesInput(),
        validators=[InputRequired(message="Please select an option")],
        choices=[("one", "One"), ("two", "Two"), ("three", "Three")],
        description="SelectMultipleFieldHint",
    )

    radio_field = RadioField(
        "RadioField",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Please select an option")],
        choices=[("one", "One"), ("two", "Two"), ("three", "Three")],
        description="RadioFieldHint",
    )

    file_field = FileField(
        "FileField",
        widget=GovFileInput(),
        validators=[InputRequired(message="Please upload a file")],
        description="FileFieldHint",
    )

    multiple_file_field = MultipleFileField(
        "MultipleFileField",
        widget=GovFileInput(multiple=True),
        validators=[InputRequired(message="Please upload a file")],
        description="MultipleFileFieldHint",
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
        description="PasswordFieldHint",
    )

    password_retype_field = PasswordField(
        "Re-type your password",
        widget=GovPasswordInput(),
        validators=[InputRequired("Please retype your password")],
        description="PasswordFieldHint",
    )

    nested_form = FieldList(
        FormField(ExampleChildForm),
        min_entries=1,
    )

    submit_button = SubmitField("SubmitField", widget=GovSubmitInput())

    def validate_string_field(self, field):
        if field.data != "John Smith":
            raise ValidationError('Example serverside error - type "John Smith" into this field to suppress it')
