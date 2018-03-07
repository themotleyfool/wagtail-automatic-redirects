import pytest


@pytest.fixture
def site():
    from wagtail.wagtailcore.models import Site
    site = Site.objects.get(is_default_site=True)
    return site
