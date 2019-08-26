from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class AutomaticRedirectsTestIndexPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, default='')
    body = RichTextField(blank=True, default='')

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]


class AutomaticRedirectsTestPage(Page):
    body = RichTextField(blank=True, default='')

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
