"""REST Api wrapper."""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from closestwins.models.question import Question


class RetrySession:  # pylint: disable=too-few-public-methods
    """Session object with retry capabilities."""

    def __init__(self):
        self.session = None

    def _requests_retry_session(
        self, retries=5, backoff_factor=2, status_forcelist=(500, 502, 503, 504)
    ):
        """Returns a retriable session"""
        if self.session:
            return self.session

        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods={"GET"},
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)

        self.session = session

        return self.session

    def get(self, *args, **kwargs):
        """Get method forwarded to a session object."""
        return self._requests_retry_session().get(*args, **kwargs)


class QuestionsApi:
    """Questions service api wrapper."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = RetrySession()

    def _get_from_api(self, resource, params=None):
        response = self.session.get(f"{self.base_url}/{resource}", params=params)
        response.raise_for_status()
        if response.text:
            return response.json()
        return {}

    def get_random_question(self):
        """Returns a random question."""
        response = self._get_from_api("question-random")
        return Question(**response)

    def get_question(self, question_id):
        """Returns a question by its id."""
        response = self._get_from_api(f"questions/{question_id}")
        return Question(**response)
