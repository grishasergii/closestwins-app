"""Smoke tests."""
from http import HTTPStatus


def test_app_can_start_and_open_index_page_returns_200(mock_api_server, app_client):
    """Test that the app can start and open the index page without an error."""
    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK
