import glob
import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

templates = []
directories = glob.glob("govuk_frontend_wtf/templates/*.html")
for directory in directories:
    templates.append(os.path.relpath(os.path.dirname(directory), "govuk_frontend_wtf") + "/*.html")

setuptools.setup(
    name="govuk-frontend-wtf",
    version="2.4.0",
    author="Matt Shaw",
    author_email="matthew.shaw@landregistry.gov.uk",
    description="GOV.UK Frontend WTForms Widgets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LandRegistry/govuk-frontend-wtf",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"govuk_frontend_wtf": templates},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.7",
    install_requires=[
        "deepmerge",
        "flask",
        "flask-wtf",
        "govuk-frontend-jinja>=2.0.0",
        "jinja2",
        "wtforms",
    ],
)
