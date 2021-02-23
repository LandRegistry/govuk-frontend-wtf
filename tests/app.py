from flask import Flask
from govuk_frontend_wtf.main import WTFormsHelpers
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

app = Flask(__name__)
app.config["SECRET_KEY"] = "M15zC@#&nMMj@J91IONM3CVubJDVIh$H"

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
