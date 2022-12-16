# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/LandRegistry/govuk-frontend-wtf/compare/2.2.0..main)

## [2.2.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/2.2.0) - 16/12/2022

### Added

- [GOV.UK Frontend v4.4.0](https://github.com/alphagov/govuk-frontend/releases/tag/v4.4.0) support
- Python 3.11 support

## [2.1.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/2.1.0) - 22/07/2022

### Added

- [GOV.UK Frontend v4.2.0](https://github.com/alphagov/govuk-frontend/releases/tag/v4.2.0) support

## [2.0.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/2.0.0) - 13/01/2022

### Added

- [GOV.UK Frontend v4.0.0](https://github.com/alphagov/govuk-frontend/releases/tag/v4.0.0) support

### Removed

- Python 3.6 support

## [1.2.1](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/1.2.1) - 08/12/2021

### Fixed

From [#38](https://github.com/LandRegistry/govuk-frontend-wtf/pull/38), thanks to [Dale Potter](https://github.com/dalepotter)

- `ValueError` when parsing edge-case `GovDateInput` input data
- Removes call to a private WTForm `Field` method.
- Ensures user-inputted data (i.e. `Field.raw_data`) always takes precedence over default values (i.e. `Field.data`)

## [1.2.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/1.2.0) - 23/11/2021

### Added

- `GovCharacterCount` widget to render text area fields with character counts. Thanks to [Matt Pease](https://github.com/Skablam)

## [1.1.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/1.1.0) - 11/11/2021

### Added

- Support for WTForms v3.0.0

### Fixed

- Removed deprecated `jinja2.Markup` call in favour of `markupsafe.Markup`, which resolves all deprecation warnings from test execution

## [1.0.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/1.0.0) - 22/10/2021

### Added

- Form field descriptions are automatically added as hint text
- Support for [Python v3.10](https://www.python.org/downloads/release/python-3100/)

### Changed

- Support for [GOV.UK Frontend v3.14.0](https://github.com/alphagov/govuk-frontend/releases/tag/v3.14.0) via [GOV.UK Frontend Jinja v1.5.1](https://github.com/LandRegistry/govuk-frontend-jinja/releases/tag/1.5.1)
- Restricted future version requirements of GOV.UK Frontend Jinja to <2.0.0 to maintain compatibility with GOV.UK Frontend v3.x.x (both GOV.UK Frontend Jinja and GOV.UK Frontend WTForms will move to v2.x.x when GOV.UK Frontend v4.x.x is released)

### Fixed

- `GovCheckboxesInput` have the `aria-describedby` attribute added to their fieldset, not the input
- `GovCheckboxInput` have the inherited fieldset removed, so that the `aria-describedby` attribute is added to the input

## [0.3.2](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/0.3.2) - 01/06/2021

### Fixed

- Set day, month, year values to None if no value is provided

## [0.3.1](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/0.3.1) - 28/05/2021

### Fixed

- Ensure day, month, year values are set when default provided for GovDateInput

## [0.3.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/0.3.0) - 13/05/2021

### Added

- Support flattening errors from FieldList/FormField for display in the error summary.

### Fixed

- Use field label as fieldset legend by default for `GovRadioInput`

## [0.2.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/0.2.0) - 05/05/2021

### Added

- `GovDateInput` widget to render WTForms [DateField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DateField) and [DateTimeFields](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DateTimeField) as [GOV.UK Date input components](https://design-system.service.gov.uk/components/date-input/). Thanks to [Hugo Baldwin](https://github.com/byzantime) and [Dale Potter](https://github.com/dalepotter)

### Changed

- Exclude tests directory from built package

## [0.1.1](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/0.1.1) - 05/03/2021

### Added

- Clarification that this is a [GOV.UK Design System Community Resource](https://design-system.service.gov.uk/community/resources-and-tools/), created and maintained by HM Land Registry
- Issue templates for [bug reports](.github/ISSUE_TEMPLATE/bug_report.md) and [feature requests](.github/ISSUE_TEMPLATE/feature_request.md)
- Dependabot config to help keep requirements up to date
- [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md)
- [Contribution guidelines](CONTRIBUTING.md)
- [Support information](README.md#support)

## [0.1.0](https://github.com/LandRegistry/govuk-frontend-wtf/releases/tag/0.1.0) - 23/02/2021

### Added

- Refactored from internal source code into publicly available package.

### Fixed

- Error summary links were linked to the error message not linked to the corresponding input. Now corrected.
