from setuptools import setup, find_packages
from os import path

install_requires = ["wagtail"]

tests_require = ["pytest-django", "wagtail-factories", "pytest"]

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    version="1.1.0",
    name="wagtail-automatic-redirects",
    description="Helpers for Wagtail Redirects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Parbhat Puri",
    author_email="me@parbhatpuri.com",
    url="https://github.com/themotleyfool/wagtail-automatic-redirects",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Wagtail",
    ],
    setup_requires=["setuptools_scm", "pytest-runner"],
    python_requires=">=3.6",
)
