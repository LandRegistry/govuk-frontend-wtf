from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

from govuk_frontend_wtf.main import WTFormsHelpers

app = Flask(__name__)
app.config["SECRET_KEY"] = "405eb39c8ab0d1ab4a4ff56657a0d7aebf8ed079d4c5466a4933c72703a135f6"  # nosec

app.jinja_loader = ChoiceLoader(
    [
        PrefixLoader(
            {
                "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                "govuk_frontend_wtf": PackageLoader("govuk_frontend_wtf"),
            }
        ),
    ]
)

WTFormsHelpers(app)
