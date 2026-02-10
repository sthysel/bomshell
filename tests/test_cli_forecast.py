import json
from unittest.mock import patch

import requests
from typer.testing import CliRunner

from bomshell.cli import app

LOCATIONS_ONE = [{"geohash": "r1r0fsp", "name": "Roleystone", "postcode": "6111", "state": "WA"}]
LOCATIONS_MULTI = [
    {"geohash": "r1r0fsp", "name": "Roleystone", "postcode": "6111", "state": "WA"},
    {"geohash": "r1r11g6", "name": "Roleystone South", "postcode": "6111", "state": "WA"},
]
FORECAST_DATA = {
    "data": [
        {
            "date": "2025-02-11",
            "short_text": "Mostly sunny.",
            "extended_text": "Light winds.",
            "temp_max": 29,
            "temp_min": 16,
            "rain": {"chance": 5},
            "uv": {"category": "Extreme", "max_index": 12},
            "fire_danger": "High",
        }
    ]
}


class TestForecastCommand:
    def test_single_match(self):
        with (
            patch("bomshell.forecast.search_location", return_value=LOCATIONS_ONE) as mock_search,
            patch("bomshell.forecast.get_daily_forecast", return_value=FORECAST_DATA) as mock_fc,
        ):
            runner = CliRunner()
            result = runner.invoke(app, ["forecast", "Roleystone"])

            assert result.exit_code == 0
            mock_search.assert_called_once_with("Roleystone")
            mock_fc.assert_called_once_with("r1r0fsp")
            assert "Roleystone, WA 6111" in result.output
            assert "Mostly sunny." in result.output

    def test_multiple_matches_shows_list(self):
        with (
            patch("bomshell.forecast.search_location", return_value=LOCATIONS_MULTI),
            patch("bomshell.forecast.get_daily_forecast", return_value=FORECAST_DATA),
        ):
            runner = CliRunner()
            result = runner.invoke(app, ["forecast", "Roleystone"])

            assert result.exit_code == 0
            assert "Found 2 matches" in result.output
            assert "1. Roleystone" in result.output
            assert "2. Roleystone South" in result.output

    def test_no_matches(self):
        with patch("bomshell.forecast.search_location", return_value=[]):
            runner = CliRunner()
            result = runner.invoke(app, ["forecast", "nonexistent_xyz"])

            assert result.exit_code != 0
            assert "No locations found" in result.output

    def test_search_api_error(self):
        with patch("bomshell.forecast.search_location", side_effect=requests.HTTPError("500")):
            runner = CliRunner()
            result = runner.invoke(app, ["forecast", "Roleystone"])

            assert result.exit_code != 0
            assert "Error searching" in result.output

    def test_forecast_api_error(self):
        with (
            patch("bomshell.forecast.search_location", return_value=LOCATIONS_ONE),
            patch("bomshell.forecast.get_daily_forecast", side_effect=requests.ConnectionError("timeout")),
        ):
            runner = CliRunner()
            result = runner.invoke(app, ["forecast", "Roleystone"])

            assert result.exit_code != 0
            assert "Error fetching forecast" in result.output

    def test_default_town_is_roleystone(self):
        with (
            patch("bomshell.forecast.search_location", return_value=LOCATIONS_ONE) as mock_search,
            patch("bomshell.forecast.get_daily_forecast", return_value=FORECAST_DATA),
        ):
            runner = CliRunner()
            result = runner.invoke(app, ["forecast"])

            assert result.exit_code == 0
            mock_search.assert_called_once_with("Roleystone")

    def test_forecast_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["forecast", "--help"])

        assert result.exit_code == 0
        assert "7-day weather forecast" in result.output

    def test_json_forecast(self):
        with (
            patch("bomshell.forecast.search_location", return_value=LOCATIONS_ONE),
            patch("bomshell.forecast.get_daily_forecast", return_value=FORECAST_DATA),
        ):
            runner = CliRunner()
            result = runner.invoke(app, ["--json", "forecast", "Roleystone"])

            assert result.exit_code == 0
            data = json.loads(result.output)
            assert "location" in data
            assert "forecast" in data
            assert data["location"]["name"] == "Roleystone"
