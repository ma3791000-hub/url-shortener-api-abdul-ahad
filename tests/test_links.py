
def test_create_short_link(client):
    response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_url"] == "https://example.com/"
    assert len(data["code"]) == 7
    assert data["short_url"].endswith("/" + data["code"])


def test_duplicate_custom_alias(client):
    first_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "test123",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/links/",
        json={
            "url": "https://wikipedia.org",
            "custom_alias": "test123",
        },
    )

    assert second_response.status_code == 409

def test_unknown_short_link_returns_404(client):
    response = client.get(
        "/notfound123",
        follow_redirects=False,
    )

    assert response.status_code == 404

def test_expired_link_returns_410(client):
    response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "oldtest",
            "expires_at": "2020-01-01T10:00:00",
        },
    )

    assert response.status_code == 201

    redirect_response = client.get(
        "/oldtest",
        follow_redirects=False,
    )

    assert redirect_response.status_code == 410

def test_list_links_pagination(client):
    for number in range(3):
        response = client.post(
            "/api/links/",
            json={
                "url": f"https://example.com/page{number}",
                "custom_alias": f"page{number}1",
            },
        )
        assert response.status_code == 201

    response = client.get(
        "/api/links/?page=1&page_size=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert len(data["links"]) == 2

def test_delete_link(client):
    create_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "delete1",
        },
    )

    assert create_response.status_code == 201

    delete_response = client.delete(
        "/api/links/delete1"
    )

    assert delete_response.status_code == 200

    get_response = client.get(
        "/api/links/"
    )

    assert get_response.status_code == 200

    codes = [
        link["code"]
        for link in get_response.json()["links"]
    ]

    assert "delete1" not in codes

def test_link_stats(client):
    create_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "stats01",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/links/stats01/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_clicks"] == 0
    assert "clicks_per_day" in data
    assert "top_referrers" in data
def test_redirect_records_click(client):
    create_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "click01",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/click01",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/"

    stats_response = client.get(
        "/api/links/click01/stats"
    )

    assert stats_response.status_code == 200
    assert stats_response.json()["total_clicks"] == 1
def test_delete_link_removes_click_data(client):
    create_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "delclick",
        },
    )

    assert create_response.status_code == 201

    client.get(
        "/delclick",
        follow_redirects=False,
    )

    stats_response = client.get(
        "/api/links/delclick/stats"
    )

    assert stats_response.json()["total_clicks"] == 1

    delete_response = client.delete(
        "/api/links/delclick"
    )

    assert delete_response.status_code == 200

    redirect_response = client.get(
        "/delclick",
        follow_redirects=False,
    )

    assert redirect_response.status_code == 404

def test_invalid_url_is_rejected(client):
    response = client.post(
        "/api/links/",
        json={
            "url": "ftp://example.com",
        },
    )

    assert response.status_code == 422
def test_redirect_records_user_agent_and_referrer(client):
    create_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "track01",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/track01",
        headers={
            "User-Agent": "TestBrowser/1.0",
            "Referer": "https://google.com",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    from app.database import get_db
    from app.main import app
    from app.models import Click, Link

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)

    try:
        link = db.query(Link).filter(
            Link.code == "track01"
        ).first()

        click = db.query(Click).filter(
            Click.link_id == link.id
        ).first()

        assert click is not None
        assert click.user_agent == "TestBrowser/1.0"
        assert click.referrer == "https://google.com"

    finally:
        db.close()
        db_generator.close()
def test_link_stats_returns_seven_days(client):
    create_response = client.post(
        "/api/links/",
        json={
            "url": "https://example.com",
            "custom_alias": "stats01"
        }
    )

    assert create_response.status_code == 201

    response = client.get("/api/links/stats01/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == "stats01"
    assert data["total_clicks"] == 0
    assert len(data["clicks_per_day"]) == 7