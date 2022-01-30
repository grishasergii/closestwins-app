"""Global fixtures."""
import time

import docker
import pytest

from closestwins import create_app


@pytest.fixture(autouse=True)
def testing_env(monkeypatch):
    """Set ENV variables for testing."""
    monkeypatch.setenv("FLASK_ENV", "development")
    monkeypatch.setenv("MAP_API_KEY", "dummy")
    monkeypatch.setenv("QUESTIONS_API_URL", "http://127.0.0.1:5002")


@pytest.fixture(scope="module")
def mock_api_server():
    """Starts a mock api server in a docker container."""
    image_name = "mock-api-server-fixture"
    client = docker.from_env()
    client.images.build(path="tests/mock_api_server", tag=image_name)
    container = client.containers.run(
        image=image_name,
        auto_remove=True,
        detach=True,
        ports={5000: 5002},
        name=image_name,
    )
    time.sleep(2)

    yield

    container.kill()


@pytest.fixture()
def app_client():
    """Creates an app test client."""
    app = create_app()
    with app.test_client() as client:
        yield client
