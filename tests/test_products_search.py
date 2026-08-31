import pytest

@pytest.mark.django_db
def test_product_search_by_title(
    client,
    product
):
    response = client.get(
        "/api/search/products/?q=iphone"
    )

    assert response.status_code == 200

    titles = [
        item["title"]
        for item in response.data["results"]
    ]

    assert "iPhone" in titles


@pytest.mark.django_db
def test_product_suggest_minimum_characters(client):
    response = client.get(
        "/api/search/suggest/?q=ip"
    )

    assert response.status_code == 400

    assert response.data["detail"] == (
        "Search query must contain at least 3 characters."
    )