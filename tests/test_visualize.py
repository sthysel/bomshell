from unittest.mock import patch

import pytest

from bomshell.visualize import SPATIAL_CONFIGS
from bomshell.visualize import _build_popup_html
from bomshell.visualize import get_visualizable_types


class TestGetVisualizableTypes:
    def test_returns_sorted_list(self):
        types = get_visualizable_types()
        assert types == sorted(types)

    def test_contains_known_types(self):
        types = get_visualizable_types()
        assert "radar_location" in types
        assert "forecast_districts" in types
        assert "point_places" in types


class TestBuildPopupHtml:
    def test_basic_popup(self):
        record = {"Name": "Perth", "State": "WA"}
        html = _build_popup_html(record, ["Name", "State"])
        assert "<b>Name:</b> Perth" in html
        assert "<b>State:</b> WA" in html

    def test_missing_fields_skipped(self):
        record = {"Name": "Perth"}
        html = _build_popup_html(record, ["Name", "Missing"])
        assert "Perth" in html
        assert "Missing" not in html

    def test_empty_fields_skipped(self):
        record = {"Name": "", "State": "WA"}
        html = _build_popup_html(record, ["Name", "State"])
        assert "Name" not in html
        assert "State" in html

    def test_empty_record(self):
        html = _build_popup_html({}, ["A", "B"])
        assert html == ""


class TestSpatialConfigs:
    def test_all_configs_have_required_keys(self):
        for name, config in SPATIAL_CONFIGS.items():
            assert "file" in config, f"{name} missing 'file'"
            assert "type" in config, f"{name} missing 'type'"
            assert "name" in config, f"{name} missing 'name'"
            assert "popup_fields" in config, f"{name} missing 'popup_fields'"
            assert "label" in config, f"{name} missing 'label'"
            assert config["type"] in ("point", "polygon"), f"{name} has invalid type"

    def test_point_configs_have_lat_lon(self):
        for name, config in SPATIAL_CONFIGS.items():
            if config["type"] == "point":
                assert "lat" in config, f"{name} missing 'lat'"
                assert "lon" in config, f"{name} missing 'lon'"
                assert "color" in config, f"{name} missing 'color'"
                assert "icon" in config, f"{name} missing 'icon'"

    def test_polygon_configs_have_colors(self):
        for name, config in SPATIAL_CONFIGS.items():
            if config["type"] == "polygon":
                assert "fill_color" in config, f"{name} missing 'fill_color'"
                assert "line_color" in config, f"{name} missing 'line_color'"


class TestOpenInBrowser:
    @patch("bomshell.visualize.webbrowser.open")
    def test_opens_file_url(self, mock_open):
        from bomshell.visualize import open_in_browser

        open_in_browser("/tmp/test.html")
        mock_open.assert_called_once()
        url = mock_open.call_args[0][0]
        assert url.startswith("file://")
        assert "test.html" in url


class TestCreateMap:
    @patch("bomshell.visualize._add_layer")
    def test_single_type_default_output(self, mock_add_layer, tmp_path):
        from bomshell import settings
        from bomshell.visualize import create_map

        old_cache = settings.CACHE
        try:
            settings.CACHE = str(tmp_path)
            path = create_map("radar_location")
            assert path.endswith("radar_location.html")
            mock_add_layer.assert_called_once()
        finally:
            settings.CACHE = old_cache

    @patch("bomshell.visualize._add_layer")
    def test_multiple_types(self, mock_add_layer, tmp_path):
        from bomshell import settings
        from bomshell.visualize import create_map

        old_cache = settings.CACHE
        try:
            settings.CACHE = str(tmp_path)
            path = create_map(["radar_location", "forecast_districts"])
            assert path.endswith("combined_map.html")
            assert mock_add_layer.call_count == 2
        finally:
            settings.CACHE = old_cache

    @patch("bomshell.visualize._add_layer")
    def test_custom_output_path(self, mock_add_layer, tmp_path):
        from bomshell.visualize import create_map

        out = str(tmp_path / "custom.html")
        path = create_map("radar_location", output_path=out)
        assert path == out

    def test_unknown_type_raises(self):
        from bomshell.visualize import create_map

        with pytest.raises(ValueError, match="Unknown spatial type"):
            create_map("totally_fake_type")

    @patch("bomshell.visualize._add_layer")
    def test_polygons_rendered_before_points(self, mock_add_layer, tmp_path):
        from bomshell import settings
        from bomshell.visualize import create_map

        old_cache = settings.CACHE
        try:
            settings.CACHE = str(tmp_path)
            create_map(["radar_location", "forecast_districts"])
            calls = [c[0][1] for c in mock_add_layer.call_args_list]
            # polygon type should come first
            assert calls == ["forecast_districts", "radar_location"]
        finally:
            settings.CACHE = old_cache
