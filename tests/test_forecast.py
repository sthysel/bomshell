from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import requests

from bomshell.forecast import BOM_API_BASE
from bomshell.forecast import format_forecast
from bomshell.forecast import get_daily_forecast
from bomshell.forecast import search_location


@pytest.fixture()
def single_location():
    return {
        "geohash": "r1r0fsp",
        "name": "Roleystone",
        "postcode": "6111",
        "state": "WA",
    }


@pytest.fixture()
def forecast_data():
    return {
        "data": [
            {
                "date": "2025-02-11",
                "short_text": "Mostly sunny.",
                "extended_text": "Mostly sunny. Winds southeasterly 25 to 40 km/h.",
                "temp_max": 29,
                "temp_min": 16,
                "rain": {"chance": 5},
                "uv": {"category": "Extreme", "max_index": 12},
                "fire_danger": "High",
            },
            {
                "date": "2025-02-12",
                "short_text": "Sunny.",
                "extended_text": "Sunny. Light winds.",
                "temp_max": 33,
                "temp_min": 17,
                "rain": {"chance": 0},
                "uv": {"category": "Very High", "max_index": 10},
                "fire_danger": None,
            },
        ]
    }


class TestSearchLocation:
    @patch("bomshell.forecast._SESSION")
    def test_returns_parsed_locations(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "data": [
                {"geohash": "r1r0fsp", "name": "Roleystone", "postcode": "6111", "state": "WA"},
                {"geohash": "r1r11g6", "name": "Roleystone South", "postcode": "6111", "state": "WA"},
            ]
        }
        mock_session.get.return_value = mock_resp

        results = search_location("Roleystone")

        mock_session.get.assert_called_once_with(f"{BOM_API_BASE}/locations", params={"search": "Roleystone"})
        mock_resp.raise_for_status.assert_called_once()
        assert len(results) == 2
        assert results[0]["geohash"] == "r1r0fsp"
        assert results[0]["name"] == "Roleystone"

    @patch("bomshell.forecast._SESSION")
    def test_returns_empty_list_for_no_matches(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"data": []}
        mock_session.get.return_value = mock_resp

        results = search_location("nonexistent_place_xyz")
        assert results == []

    @patch("bomshell.forecast._SESSION")
    def test_missing_optional_fields(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"data": [{"geohash": "abc123", "name": "SomePlace"}]}
        mock_session.get.return_value = mock_resp

        results = search_location("SomePlace")
        assert results[0]["postcode"] == ""
        assert results[0]["state"] == ""

    @patch("bomshell.forecast._SESSION")
    def test_raises_on_http_error(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        mock_session.get.return_value = mock_resp

        with pytest.raises(requests.HTTPError):
            search_location("Roleystone")


class TestGetDailyForecast:
    @patch("bomshell.forecast._SESSION")
    def test_returns_forecast_json(self, mock_session):
        expected = {"data": [{"date": "2025-02-11"}]}
        mock_resp = MagicMock()
        mock_resp.json.return_value = expected
        mock_session.get.return_value = mock_resp

        result = get_daily_forecast("r1r0fsp")

        mock_session.get.assert_called_once_with(f"{BOM_API_BASE}/locations/r1r0fsp/forecasts/daily")
        mock_resp.raise_for_status.assert_called_once()
        assert result == expected

    @patch("bomshell.forecast._SESSION")
    def test_raises_on_http_error(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("404")
        mock_session.get.return_value = mock_resp

        with pytest.raises(requests.HTTPError):
            get_daily_forecast("bad_hash")


class TestFormatForecast:
    def test_full_forecast(self, single_location, forecast_data):
        output = format_forecast(single_location, forecast_data)

        assert "Roleystone, WA 6111" in output
        assert "Tue 11 Feb" in output
        assert "Mostly sunny." in output
        assert "29\u00b0/16\u00b0" in output
        assert "Rain: 5% chance" in output
        assert "UV: Extreme (12)" in output
        assert "Fire: High" in output
        assert "Wed 12 Feb" in output
        assert "Sunny." in output

    def test_no_fire_danger_omitted(self, single_location, forecast_data):
        output = format_forecast(single_location, forecast_data)
        # Second day has fire_danger=None so "Fire:" should only appear once
        lines_with_fire = [line for line in output.splitlines() if "Fire:" in line]
        assert len(lines_with_fire) == 1

    def test_header_without_state(self):
        location = {"name": "Mystery", "postcode": "1234"}
        output = format_forecast(location, {"data": []})
        assert output.startswith("Mystery 1234")

    def test_header_without_postcode(self):
        location = {"name": "Mystery", "state": "NSW"}
        output = format_forecast(location, {"data": []})
        assert output.startswith("Mystery, NSW")

    def test_header_name_only(self):
        location = {"name": "Mystery"}
        output = format_forecast(location, {"data": []})
        assert output.startswith("Mystery")
        assert "," not in output.splitlines()[0]

    def test_empty_forecast_data(self, single_location):
        output = format_forecast(single_location, {"data": []})
        assert "Roleystone, WA 6111" in output

    def test_temp_max_only(self, single_location):
        data = {"data": [{"date": "2025-02-11", "short_text": "Hot.", "temp_max": 40, "temp_min": None}]}
        output = format_forecast(single_location, data)
        assert "40\u00b0" in output
        assert "/" not in output.split("Hot.")[1].split("\n")[0]

    def test_no_temps(self, single_location):
        data = {"data": [{"date": "2025-02-11", "short_text": "Cloudy."}]}
        output = format_forecast(single_location, data)
        assert "\u00b0" not in output

    def test_no_short_text_uses_date_only(self, single_location):
        data = {"data": [{"date": "2025-02-11"}]}
        output = format_forecast(single_location, data)
        assert "Tue 11 Feb" in output
        assert "\u2014" not in output

    def test_invalid_date_falls_back_to_raw_string(self, single_location):
        data = {"data": [{"date": "not-a-date", "short_text": "Fine."}]}
        output = format_forecast(single_location, data)
        assert "not-a-date" in output

    def test_uv_without_max_index(self, single_location):
        data = {
            "data": [
                {
                    "date": "2025-02-11",
                    "uv": {"category": "Low", "max_index": None},
                }
            ]
        }
        output = format_forecast(single_location, data)
        assert "UV: Low" in output
        assert "(None)" not in output
