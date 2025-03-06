from typing import Any, Dict, List, Union

from deepmerge import Merger
from wtforms import Form, ValidationError


class WTFormsHelpers:
    """
    Provides helper functions for integrating WTForms with GOV.UK Frontend templates.

    This class registers a template global function (`wtforms_errors`) that simplifies
    the process of displaying WTForms errors within GOV.UK Frontend error summaries.
    """

    def __init__(self, app: Any = None) -> None:
        """Initializes the WTFormsHelpers instance.

        Args:
            app: The Flask application instance (optional). If provided, the helper
                 function is registered as a template global.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Any) -> None:
        """Registers the `wtforms_errors` function as a template global."""
        app.add_template_global(wtforms_errors)


def wtforms_errors(form: Form, params: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Generates a dictionary of WTForms errors formatted for GOV.UK Frontend error summaries.

    This function takes a WTForms form instance and processes its errors to create a
    dictionary suitable for use with the GOV.UK Frontend error summary macro.  It
    includes functionality to map error messages to specific field IDs.

    Args:
        form: The WTForms form containing errors.
        params: Optional additional parameters to merge into the result.

    Returns:
        A dictionary containing the formatted error information, ready to be used
        in a GOV.UK Frontend template.
    """
    wtforms_params: Dict[str, Any] = {
        "titleText": "There is a problem",  # Default title for error summary
        "errorList": [],  # List to hold individual error messages
    }

    id_map: Dict[str, str] = {}  # Map field names to their IDs
    for field_name, field in form._fields.items():
        if hasattr(field, "id"):
            id_map[field_name] = field.id  # type: ignore[assignment]

    wtforms_params["errorList"] = flatten_errors(form.errors, id_map=id_map)

    return merger.merge(wtforms_params, params)  # Merge with additional parameters


def flatten_errors(
    errors: Union[List[Any], Dict[str, Any], ValidationError],
    prefix: str = "",
    id_map: Dict[str, str] = {},
) -> List[Dict[str, str]]:
    """
    Recursively flattens a nested WTForms error structure into a list of dictionaries.

    This function processes the potentially nested structure of WTForms errors,
    creating a flat list of dictionaries where each dictionary represents a single
    error message with its associated field ID (or a generic error if no field is
    specified).

    Args:
        errors: The WTForms error structure (can be a dictionary, list, or ValidationError).
        prefix: A prefix string to prepend to field names (used for recursive calls).
        id_map: A dictionary mapping field names to their corresponding IDs.

    Returns:
        A list of dictionaries, where each dictionary contains 'text' (the error message)
        and 'href' (a link to the field with the error).
    """
    error_list: List[Dict[str, str]] = []
    if isinstance(errors, dict):
        for key, value in errors.items():
            key_with_id = id_map.get(key, key)
            prefix_new = f"{prefix}{key_with_id}-"
            error_list.extend(flatten_errors(value, prefix=prefix_new, id_map=id_map))
    elif isinstance(errors, list):
        if isinstance(errors[0], dict):
            for idx, error in enumerate(errors):
                prefix_new = f"{prefix}{idx}-"
                error_list.extend(flatten_errors(error, prefix=prefix_new, id_map=id_map))
        else:
            error_list.append({"text": str(errors[0]), "href": f"#{prefix.rstrip('-')}"})
    elif isinstance(errors, ValidationError):
        error_list.append({"text": str(errors), "href": f"#{prefix.rstrip('-')}"})
    else:
        error_list.append({"text": str(errors), "href": f"#{prefix.rstrip('-')}"})

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
