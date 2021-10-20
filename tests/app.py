from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

from govuk_frontend_wtf.main import WTFormsHelpers

app = Flask(__name__)
app.config["SECRET_KEY"] = "M15zC@#&nMMj@J91IONM3CVubJDVIh$H"  # nosec

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
