from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (2, 0):
    from wagtail.core.signals import page_published
    from wagtail.contrib.redirects.models import Redirect

    if WAGTAIL_VERSION >= (2, 10):
        from wagtail.core.signals import post_page_move
    else:
        post_page_move = None
else:
    from wagtail.wagtailcore.signals import page_published
    from wagtail.wagtailredirects.models import Redirect


# Create redirect from old slug to new if slug changed in published page.
# Redirect will be created for Page and all it's children.
# It will not work when page moved in the site tree.
def create_redirect_object_if_slug_changed(sender, **kwargs):
    instance = kwargs['instance']

    # The main part is getting the old URL from which the redirect is required.
    # Wagtail keeps the record of every page change in terms of revisions.
    # This will help to keep track of every change made to page including
    # page slug. The next part is determining the revision is for draft or
    # published page. For example, an admin user start editing the page
    # (with slug /original) change Url (/original-changed) and save as draft.
    # On next edit, user again change the URL to something else
    # (/original-desired) and then publish the page. So, in this case, redirect
    # should be created from /original to /original-desired. Page object that
    # has has_unpublished_changes value True, is draft revision. Interestingly
    # when admin user edit a page, user is editing the page object created from
    # JSON and value is stored as JSON in revision.
    page_revisions = instance.revisions.order_by('-created_at', '-id')
    for revision in page_revisions:
        page_obj = revision.page.specific_class.from_json(
            revision.content_json)

        # The first revision's page object that has has_published_changes
        # value False is the last published Page.
        if not page_obj.has_unpublished_changes:
            # Only create redirect if slug change
            if instance.url != page_obj.url:
                old_path = Redirect.normalise_path(page_obj.url)
                Redirect.objects.update_or_create(
                    old_path=old_path,
                    defaults={
                        'redirect_page': instance
                    }
                )
                # Also create redirect objects for children of this Page
                create_redirect_objects_for_children(old_path, page_obj)
            break


def create_redirect_object_after_page_move(sender, **kwargs):
    if kwargs['url_path_before'] == kwargs['url_path_after']:
        return

    page_after = kwargs['instance']
    parent_page_before_url = kwargs['parent_page_before'].get_url()
    page_before_url = Redirect.normalise_path(
        parent_page_before_url + page_after.slug
    )
    Redirect.objects.update_or_create(
        old_path=page_before_url,
        defaults={
            'redirect_page': page_after
        }
    )

    create_redirect_objects_for_children(page_before_url, page_after)


# Register receivers
def register_signal_handlers():
    page_published.connect(create_redirect_object_if_slug_changed)

    if post_page_move is not None:
        post_page_move.connect(create_redirect_object_after_page_move)


def create_redirect_objects_for_children(parent_old_slug, parent):
    if not parent.get_children():
        return
    else:
        for child_page in parent.get_children():
            old_path = Redirect.normalise_path(
                parent_old_slug + '/' + child_page.slug)
            Redirect.objects.update_or_create(
                old_path=old_path,
                defaults={
                    'redirect_page': child_page
                }
            )

            create_redirect_objects_for_children(old_path, child_page)
