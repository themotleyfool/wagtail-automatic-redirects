# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticRedirectsTestIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(on_delete=models.deletion.CASCADE, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(default=b'', max_length=255, blank=True)),
                ('body', wagtail.core.fields.RichTextField(default=b'', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AutomaticRedirectsTestPage',
            fields=[
                ('page_ptr', models.OneToOneField(on_delete=models.deletion.CASCADE, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(default=b'', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
