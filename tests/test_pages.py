import pytest

from wagtail import VERSION as WAGTAIL_VERSION

from tests.testapp import factories


def publish_page(page):
    revision = page.save_revision()
    revision.publish()
    return page


@pytest.mark.django_db
def test_index_page_slug_change(client, site):
    test_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
        parent=site.root_page,
        title='Automatic redirects test index page',
        slug='automatic-redirects-test-index-page',
        subtitle='Test subtitle',
        body='<p>Test body</p>',
    )

    assert site.root_page.get_children().count() == 1
    assert test_index_page.slug == 'automatic-redirects-test-index-page'
    assert test_index_page.body == '<p>Test body</p>'

    response = client.get(test_index_page.url)
    assert response.status_code == 200

    # Change slug
    old_url = test_index_page.url
    test_index_page.slug = 'test-index-page'
    publish_page(test_index_page)

    # New url will give 200
    response = client.get('/test-index-page/')
    assert response.status_code == 200

    # Old url will give 301 Permanent Redirect
    response = client.get(old_url)
    assert response.status_code == 301

    # Follow the old url to get 200
    response = client.get(old_url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_page_slug_change_create_redirects_child_pages(client, site):
    test_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
        parent=site.root_page,
        title='Automatic redirects test index page',
        slug='index-page',
        subtitle='Test subtitle',
        body='<p>Test body</p>',
    )

    test_page1 = factories.AutomaticRedirectsTestPageFactory(
        parent=test_index_page,
        title='Test Page 1',
        slug='test-page-1'
    )
    test_page2 = factories.AutomaticRedirectsTestPageFactory(
        parent=test_index_page,
        title='Test Page 2',
        slug='test-page-2'
    )

    response = client.get(test_page1.url)
    assert response.status_code == 200

    response = client.get(test_page2.url)
    assert response.status_code == 200

    # Change slug
    old_url = test_index_page.url
    test_index_page.slug = 'index-page-new'
    publish_page(test_index_page)

    # New url will give 200
    response = client.get('/index-page-new/')
    assert response.status_code == 200

    response = client.get('/index-page-new/test-page-1/')
    assert response.status_code == 200

    response = client.get('/index-page-new/test-page-2/')
    assert response.status_code == 200

    # Old urls will give 301 Permanent Redirect
    response = client.get(old_url)
    assert response.status_code == 301

    response = client.get('/index-page/test-page-1/')
    assert response.status_code == 301

    response = client.get('/index-page/test-page-2/')
    assert response.status_code == 301


@pytest.mark.skipif(
    WAGTAIL_VERSION < (2, 10),
    reason="Move signals require wagtail 2.10 or higher"
)
@pytest.mark.django_db
def test_move_page_from_one_index_to_another_creates_redirect(client, site):
    test_index_page_1 = factories.AutomaticRedirectsTestIndexPageFactory(
        parent=site.root_page,
        title='Automatic redirects test index page 1',
        slug='index-page-1',
        subtitle='Test subtitle',
        body='<p>Test body</p>',
    )

    response = client.get(test_index_page_1.get_url())
    assert response.status_code == 200

    test_index_page_2 = factories.AutomaticRedirectsTestIndexPageFactory(
        parent=site.root_page,
        title='Automatic redirects test index page 2',
        slug='index-page-2',
        subtitle='Test subtitle',
        body='<p>Test body</p>',
    )

    response = client.get(test_index_page_2.get_url())
    assert response.status_code == 200
    assert 'index-page-2' in test_index_page_2.get_url()

    test_page = factories.AutomaticRedirectsTestPageFactory(
        parent=test_index_page_1,
        title='Test Page',
        slug='test-page'
    )

    test_page_url_pre_move = test_page.get_url()
    response = client.get(test_page_url_pre_move)
    assert response.status_code == 200
    assert test_index_page_1.get_url() in test_page_url_pre_move

    test_page.move(test_index_page_2, 'last-child')
    test_page.refresh_from_db()

    test_page_url_post_move = test_page.get_url()
    assert test_index_page_1.get_descendants().count() == 0
    assert test_index_page_2.get_descendants().count() == 1
    assert test_index_page_1.get_url() not in test_page_url_post_move
    assert test_index_page_2.get_url() in test_page_url_post_move

    response = client.get(test_page_url_post_move)
    assert response.status_code == 200
    response = client.get(test_page_url_pre_move)
    assert response.status_code == 301


@pytest.mark.skipif(
    WAGTAIL_VERSION < (2, 10),
    reason="Move signals require wagtail 2.10 or higher"
)
@pytest.mark.django_db
def test_move_page_from_one_index_to_another_creates_redirect_for_child(
        client,
        site,
    ):
    test_index_page_1 = factories.AutomaticRedirectsTestIndexPageFactory(
        parent=site.root_page,
        title='Automatic redirects test index page 1',
        slug='index-page-1',
        subtitle='Test subtitle',
        body='<p>Test body</p>',
    )

    response = client.get(test_index_page_1.get_url())
    assert response.status_code == 200

    test_index_page_2 = factories.AutomaticRedirectsTestIndexPageFactory(
        parent=site.root_page,
        title='Automatic redirects test index page 2',
        slug='index-page-2',
        subtitle='Test subtitle',
        body='<p>Test body</p>',
    )

    response = client.get(test_index_page_2.get_url())
    assert response.status_code == 200

    test_page = factories.AutomaticRedirectsTestPageFactory(
        parent=test_index_page_1,
        title='Test Page',
        slug='test-page'
    )

    response = client.get(test_page.get_url())
    assert response.status_code == 200

    test_page_child = factories.AutomaticRedirectsTestPageFactory(
        parent=test_page,
        title='Test Page Child',
        slug='test-page-child'
    )

    test_page_child_url_pre_move = test_page_child.get_url()
    response = client.get(test_page_child_url_pre_move)
    assert response.status_code == 200


    test_page.move(test_index_page_2, 'last-child')

    test_page_child.refresh_from_db()
    test_page_child_url_post_move = test_page_child.get_url()

    assert test_index_page_1.get_descendants().count() == 0
    assert test_index_page_2.get_descendants().count() == 2
    assert test_index_page_1.get_url() not in test_page_child_url_post_move
    assert test_index_page_2.get_url() in test_page_child_url_post_move

    response = client.get(test_page_child_url_post_move)
    assert response.status_code == 200
    response = client.get(test_page_child_url_pre_move)
    assert response.status_code == 301
