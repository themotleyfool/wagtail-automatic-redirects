# wagtail-automatic-redirects

Package to help with Wagtail URL redirects

## Installation

```shell
pip install wagtail-automatic-redirects
```

Add the package to your project's settings

```python
INSTALLED_APPS = (
    # ... Other apps
  'wagtail_automatic_redirects',
  'wagtail.wagtailredirects',
    # ... Other apps
)
```

Also, make sure the INSTALLED_APPS setting include `'wagtail.wagtailredirects'` app from Wagtail.

## Usage

Wagtail comes with a [redirects app](http://docs.wagtail.io/en/v1.13.1/editor_manual/managing_redirects.html) which helps to manually create redirects in Wagtail admin. This helper app helps to automatically create redirects when the URL of Page is changed. Redirects will be created for the page and all its child pages automatically. This project uses the page revisions and publish signal to automate the redirects creation process. Please note that no automatic redirects will be created when a page is moved in site tree using the Move option.
