import wagtail_factories

from . import models


class AutomaticRedirectsTestIndexPageFactory(wagtail_factories.PageFactory):

    class Meta:
        model = models.AutomaticRedirectsTestIndexPage


class AutomaticRedirectsTestPageFactory(wagtail_factories.PageFactory):

    class Meta:
        model = models.AutomaticRedirectsTestPage
