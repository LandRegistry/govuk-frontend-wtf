import unittest

import yaml
from flask import render_template_string

from tests.app import app
from tests.fixtures.wtf_widgets_example_form import ExampleForm


class FlaskWtfMacroTestBase(unittest.TestCase):
    """Test the flask-wtf -> govuk widgets

    Test the output of passing flask-wtf form elements
    through the custom govuk widgets, ensuring we get
    correctly formed responses.
    """

    def setup_method(self, method):
        self.app = app.test_client()
        app.jinja_env.lstrip_blocks = True
        app.jinja_env.trim_blocks = True

        app.config["WTF_CSRF_ENABLED"] = False

    def request(self, **kwargs):
        self.ctx = app.test_request_context("/", **kwargs)
        self.ctx.push()

        self.form = ExampleForm()
        self.form.validate_on_submit()

    def teardown_method(self, method):
        self.ctx.pop()

        app.config["WTF_CSRF_ENABLED"] = True

    def render(self, template):
        """Helper method to render a snippet of a form"""
        return render_template_string(template, form=self.form).strip()


def make_test_function(template, test_data):
    def test(self):
        if "request" in test_data:
            self.request(**test_data["request"])
        else:
            self.request()

        output = self.render(template)

        if "expected_output" in test_data:
            for expectation in test_data["expected_output"]:
                self.assertRegex(output, expectation)

        if "not_expected_output" in test_data:
            for expectation in test_data["not_expected_output"]:
                self.assertNotRegex(output, expectation)

    return test


test_data = yaml.safe_load(open("tests/fixtures/wtf_widgets_data.yaml").read())

for klassname, params in test_data.items():
    methods = {}
    for test_name, test_data in params["tests"].items():
        methods[test_name] = make_test_function(params["template"], test_data)

    globals()[klassname] = type(klassname, (FlaskWtfMacroTestBase,), methods)
