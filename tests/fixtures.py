import pytest
from wagtail import VERSION as WAGTAIL_VERSION

@pytest.fixture
def site():
    if WAGTAIL_VERSION >= (3, 0):
        from wagtail.models import Site
    else:
        from wagtail.core.models import Site
    site = Site.objects.get(is_default_site=True)
    return site
