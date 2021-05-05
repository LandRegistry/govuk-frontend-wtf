# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/LandRegistry/govuk-frontend-wtf/compare/0.2.0...main)

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
