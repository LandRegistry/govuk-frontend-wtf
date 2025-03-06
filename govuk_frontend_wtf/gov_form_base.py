from typing import Any, Dict

from flask import render_template
from markupsafe import Markup
from wtforms import Field, FieldList

from govuk_frontend_wtf.main import merger


class GovFormBase:
    """
    Base class for rendering GOV.UK Frontend components using WTForms fields.

    This class provides common functionality for mapping WTForms field parameters
    to the parameters expected by GOV.UK Frontend macros.  Subclasses should
    define the `template` attribute to specify the Jinja2 template to render.
    """

    template: str  # Template filename for rendering the GOV.UK component

    def __call__(self, field: Field, **kwargs: Any) -> Markup:
        """
        Renders the GOV.UK Frontend component for the given WTForms field.

        Args:
            field: The WTForms field to render.
            **kwargs: Additional keyword arguments to pass to the template.

        Returns:
            A Markup object containing the rendered HTML.
        """
        return self.render(self.map_gov_params(field, **kwargs))

    def map_gov_params(self, field: Field, **kwargs: Any) -> Dict[str, Any]:
        """
        Maps WTForms field parameters to GOV.UK Frontend macro parameters.

        This method handles the translation of common WTForms attributes (like
        `label`, `description`, `errors`) into the structure expected by the
        GOV.UK Frontend macros.  It also merges additional keyword arguments
        provided to the `__call__` method.

        Args:
            field: The WTForms field.
            **kwargs: Additional keyword arguments.

        Returns:
            A dictionary containing the parameters for the GOV.UK Frontend macro.
        """
        params: Dict[str, Any] = {
            "id": kwargs.pop("id", None),  # Extract 'id' if present, otherwise None
            "name": field.name,  # Use the field's name attribute
            "label": {"text": field.label.text},  # Create label dict
            "attributes": {},  # Initialize attributes dictionary
            "hint": (
                {"text": field.description} if field.description else None
            ),  # Create hint dict if description exists
        }

        params["value"] = kwargs.pop("value", None)  # Extract 'value'
        params["type"] = kwargs.pop("type", None)  # Extract 'type'

        kwargs.pop("items", None)  # Remove 'items' if present

        params = self.merge_params(params, kwargs.pop("params", {}))  # Merge any extra parameters

        if field.errors:
            params["errorMessage"] = {"text": field.errors[0]}  # Add error message

        params["attributes"].update(kwargs)  # Merge remaining kwargs into attributes

        # Efficiently set boolean attributes. If value is True, use key as string
        for key, value in params["attributes"].items():
            if value is True:
                params["attributes"][key] = key

        return params

    def merge_params(self, a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        """Merges two dictionaries using the govuk_frontend_wtf merger."""
        return merger.merge(a, b)

    def render(self, params: Dict[str, Any]) -> Markup:
        """Renders the GOV.UK Frontend template with the provided parameters."""
        return Markup(render_template(self.template, params=params))


class GovIterableBase(GovFormBase):
    """
    Base class for rendering iterable GOV.UK Frontend components (e.g., checkboxes, radio buttons).

    Extends `GovFormBase` to handle WTForms `FieldList` objects, mapping them
    to the GOV.UK Frontend's item-based components.
    """

    def __call__(self, field: FieldList, **kwargs: Any) -> Markup:
        """Renders the GOV.UK Frontend iterable component for the given FieldList."""
        kwargs.setdefault("id", field.id)  # Set default id

        # Safely get flags, handle case where flags attribute might not exist
        kwargs["required"] = kwargs.get(
            "required", "required" in getattr(field, "flags", [])
        )  # Check for 'required' flag

        kwargs["items"] = [
            {
                "text": subfield.label.text,  # Text for item
                "value": subfield._value(),  # Value for item
                "checked": getattr(subfield, "checked", subfield.data),  # Checked status
            }
            for subfield in field  # Iterate through subfields
        ]

        return super().__call__(field, **kwargs)

    def map_gov_params(self, field: FieldList, **kwargs: Any) -> Dict[str, Any]:
        """
        Maps parameters for iterable fields to GOV.UK Frontend macro parameters.

        Handles merging of additional parameters passed via the 'params' keyword argument.
        """
        params: Dict[str, Any] = {
            "name": field.name,
            "items": kwargs["items"],  # type: ignore[typeddict-item]
            "hint": {"text": field.description},
        }

        if "params" in kwargs:
            extra_params: Dict[str, Any] = kwargs["params"]
            if "items" in extra_params:
                for i, item in enumerate(extra_params["items"]):  # type: ignore[typeddict-item]
                    params["items"][i] = self.merge_params(params["items"][i], item)  # type: ignore[typeddict-item]
                del extra_params["items"]
            params = self.merge_params(params, extra_params)

        if field.errors:
            params["errorMessage"] = {"text": field.errors[0]}

        return params
