import unittest
from unittest.mock import patch
from recipe.utils.random_utils import get_random

class TestRandomUtils(unittest.TestCase):

    @patch('requests.get')
    def test_get_random_success(self, mock_get):
        mock_get.return_value.text = '10'
        mock_get.return_value.raise_for_status = MagicMock()
        self.assertEqual(get_random(10), 10)

    @patch('requests.get')
    def test_get_random_failure(self, mock_get):
        mock_get.side_effect = RuntimeError('API error')
        with self.assertRaises(RuntimeError):
            get_random(10)

# RANDOM_NUMBER = 42
# NUM_SONGS = 100
#
# @pytest.fixture
# def mock_random_org(mocker):
#     # Patch the requests.get call
#     # requests.get returns an object, which we have replaced with a mock object
#     mock_response = mocker.Mock()
#     # We are giving that object a text attribute
#     mock_response.text = f"{RANDOM_NUMBER}"
#     mocker.patch("requests.get", return_value=mock_response)
#     return mock_response
#
#
# def test_get_random(mock_random_org):
#     """Test retrieving a random number from random.org."""
#     result = get_random(NUM_SONGS)
#
#     # Assert that the result is the mocked random number
#     assert result == RANDOM_NUMBER, f"Expected random number {RANDOM_NUMBER}, but got {result}"
#
#     # Ensure that the correct URL was called
#     requests.get.assert_called_once_with("https://www.random.org/integers/?num=1&min=1&max=100&col=1&base=10&format=plain&rnd=new", timeout=5)
#
# def test_get_random_request_failure(mocker):
#     """Simulate  a request failure."""
#     mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))
#
#     with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
#         get_random(NUM_SONGS)
#
# def test_get_random_timeout(mocker):
#     """Simulate  a timeout."""
#     mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)
#
#     with pytest.raises(RuntimeError, match="Request to random.org timed out."):
#         get_random(NUM_SONGS)
#
# def test_get_random_invalid_response(mock_random_org):
#     """Simulate  an invalid response (non-digit)."""
#     mock_random_org.text = "invalid_response"
#
#     with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
#         get_random(NUM_SONGS)