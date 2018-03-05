import pytest

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
