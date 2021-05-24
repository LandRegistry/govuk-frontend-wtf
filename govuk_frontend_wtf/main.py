from deepmerge import Merger


class WTFormsHelpers(object):
    """WTForms helpers

    Register some template helpers to allow developers to
    map WTForms elements to the GOV.UK jinja macros
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_template_global(wtforms_errors)


def wtforms_errors(form, params={}):
    wtforms_params = {"titleText": "There is a problem", "errorList": []}

    wtforms_params["errorList"] = flatten_errors(form.errors)

    return merger.merge(wtforms_params, params)


def flatten_errors(errors, prefix=""):
    """Return list of errors from form errors."""
    error_list = []
    if isinstance(errors, dict):
        for key, value in errors.items():
            # Recurse to handle subforms.
            error_list += flatten_errors(value, prefix=f"{prefix}{key}-")
    elif isinstance(errors, list) and isinstance(errors[0], dict):
        for idx, error in enumerate(errors):
            error_list += flatten_errors(error, prefix=f"{prefix}{idx}-")
    elif isinstance(errors, list):
        error_list.append({"text": errors[0], "href": "#{}".format(prefix.rstrip("-"))})
    else:
        error_list.append({"text": errors, "href": "#{}".format(prefix.rstrip("-"))})
    return error_list


merger = Merger(
    # pass in a list of tuple, with the
    # strategies you are looking to apply
    # to each type.
    [(list, ["append"]), (dict, ["merge"])],
    # next, choose the fallback strategies,
    # applied to all other types:
    ["override"],
    # finally, choose the strategies in
    # the case where the types conflict:
    ["override"],
)
