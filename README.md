# wagtail-automatic-redirects

Package to help with Wagtail URL redirects. Wagtail comes with a [redirects app](https://docs.wagtail.io/en/stable/editor_manual/managing_redirects.html) which helps to manually create redirects in Wagtail admin. This helper app helps to automatically create redirects when the URL of Page is changed. Redirects will be created for the page and all its child pages automatically. This project uses the page revisions and publish signal to automate the redirects creation process.

## Installation

`pip install wagtail-automatic-redirects`

Add the package to your project's settings

```python
INSTALLED_APPS = [
    # ... Other apps
    "wagtail_automatic_redirects",
    "wagtail.contrib.redirects",
    # ... Other apps
]
```

Make sure the `INSTALLED_APPS` setting include `"wagtail.contrib.redirects",` app from Wagtail.

Also, check the `MIDDLEWARE` setting include

```python
MIDDLEWARE = [
    # ... Other middlewares
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # ... Other middlewares
]
```

## License

[BSD](https://github.com/themotleyfool/wagtail-automatic-redirects/blob/master/LICENSE)
