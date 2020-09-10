"""Tests for all the logic with the exchange rates sources."""
import json
import unittest
from unittest import mock

from api import exchange
from api.app import app

MOCK_VALUE = 20.20
MOCK_BANXICO = {
    "bmx": {
        "series": [
            {
                "idSerie": "SF43718",
                "titulo": "Exchange rate pesos per US dollar something something",
                "datos": [{"fecha": "09/09/2020", "dato": str(MOCK_VALUE)}],
            }
        ]
    }
}
MOCK_FIXER = {
    "success": True,
    "timestamp": 1599695946,
    "base": "EUR",
    "date": "2020-09-10",
    "rates": {"MXN": 23.94408, "USD": 1.180491},
}


class MockRequest:
    """Mock used for the response of the API for the sources."""

    def __init__(self, json_response, status_code):
        self.json_response = json_response
        self.status_code = status_code

    def json(self):
        return self.json_response


class ExchangeTest(unittest.TestCase):
    def test_exchange_banxico(self):
        """Tests the API for Banxico."""
        mock_request = MockRequest(MOCK_BANXICO, 200)
        with mock.patch("requests.get", return_value=mock_request):
            data = exchange.get_banxico_source()
        self.assertEqual(data["value"], MOCK_VALUE)
        self.assertIsNotNone(data["source_date"])

    def test_exchange_banxico_with_error(self):
        """Tests the API for Banxico with not found error."""
        mock_request = MockRequest(MOCK_BANXICO, 404)
        with mock.patch("requests.get", return_value=mock_request):
            data = exchange.get_banxico_source()
        self.assertEqual(data["value"], 0)
        self.assertIsNone(data["source_date"])

    def test_exchange_fixer(self):
        """Tests the API for Fixer."""
        mock_request = MockRequest(MOCK_FIXER, 200)
        with mock.patch("requests.get", return_value=mock_request):
            data = exchange.get_fixer_source()
        self.assertGreater(data["value"], MOCK_VALUE)
        self.assertIsNotNone(data["source_date"])

    def test_exchange_fixer_with_error(self):
        """Tests the API for Fixer with forbidden."""
        mock_request = MockRequest(MOCK_FIXER, 403)
        with mock.patch("requests.get", return_value=mock_request):
            data = exchange.get_fixer_source()
        self.assertEqual(data["value"], 0)
        self.assertIsNone(data["source_date"])

    def test_exchange_dof(self):
        """Tests the API for Diaro Oficial source.

        Not using mock to easily identify if there is a change in the structure of the table.
        """
        data = exchange.get_dof_source()
        self.assertGreater(data["value"], 0)
        self.assertIsNotNone(data["source_date"])

    def test_exchange_dof_with_error(self):
        """Tests the API for Diaro Oficial with error."""
        mock_request = MockRequest({}, 500)
        with mock.patch("requests.get", return_value=mock_request):
            data = exchange.get_dof_source()
        self.assertEqual(data["value"], 0)
        self.assertIsNone(data["source_date"])

    def test_get_sources_endpoint(self):
        """Tests the endpoint to get all sources."""
        client = app.test_client()
        rv = client.get("/api/exchange")
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn("rates", data)
        rates = data["rates"]
        self.assertIn("banxico", rates)
        self.assertIn("diario_oficial", rates)
        self.assertIn("fixer", rates)


if __name__ == "__main__":
    unittest.main()
