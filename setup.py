from setuptools import setup, find_packages


NAME = "palogy"
VERSION = "0.0.1"
PYTHON_REQUIRES = ">=3.9"
INSTALL_REQUIRES = []

AUTHOR = "tbshiki"
AUTHOR_EMAIL = "info@tbshiki.com"
URL = "https://github.com/tbshiki/" + NAME

DESCRIPTION = "A logging utility library for Python"

LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Operating System :: OS Independent",
]
KEYWORDS = "log, logger, logging"

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=["tests*"]),
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
)
