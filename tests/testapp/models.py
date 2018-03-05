from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


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
