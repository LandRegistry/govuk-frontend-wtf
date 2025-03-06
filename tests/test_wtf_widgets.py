import unittest

import yaml
from flask import render_template_string

from tests.app import app
from tests.fixtures.wtf_widgets_example_form import ExampleForm


class FlaskWtfMacroTestBase(unittest.TestCase):
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

    def render(self, template, **kwargs):
        """Helper method to render a snippet of a form"""
        return render_template_string(template, form=self.form, **kwargs).strip()


def make_test_function(template, test_data):
    def test(self):
        if "request" in test_data:
            self.request(**test_data["request"])
        else:
            self.request()

        kwargs = test_data.get("kwargs", {})
        output = self.render(template, **kwargs)

        if "expected_output" in test_data:
            for expectation in test_data["expected_output"]:
                self.assertRegex(output, expectation)

        if "not_expected_output" in test_data:
            for expectation in test_data["not_expected_output"]:
                self.assertNotRegex(output, expectation)

        if "expected_value" in test_data:  # Check input value
            self.assertIn(test_data["expected_value"], output)

    return test


test_data = yaml.safe_load(open("tests/fixtures/wtf_widgets_data.yaml").read())

for klassname, params in test_data.items():
    methods = {}
    for test_name, test_params in params["tests"].items():
        methods[test_name] = make_test_function(params["template"], test_params)

    globals()[klassname] = type(klassname, (FlaskWtfMacroTestBase,), methods)
