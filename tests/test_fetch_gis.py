from unittest.mock import patch

from bomshell import settings
from bomshell.fetch_gis import get_gis_types
from bomshell.fetch_gis import get_source_file_name


class TestGetGisTypes:
    def test_returns_sorted_keys(self):
        types = get_gis_types()
        assert types == sorted(types)
        assert "forecast_districts" in types
        assert "radar_location" in types

    def test_returns_all_known_types(self):
        types = get_gis_types()
        assert len(types) == 11


class TestGetSourceFileName:
    def test_default_extension(self):
        name = get_source_file_name("forecast_districts")
        assert name.endswith("IDM00001.dbf")
        assert settings.SPATIAL_CACHE in name

    def test_custom_extension(self):
        name = get_source_file_name("forecast_districts", file_extention=".shp")
        assert name.endswith("IDM00001.shp")


class TestFetchSpatialData:
    @patch("bomshell.fetch_gis.fetch.get_file")
    def test_fetches_all_shapefile_components(self, mock_get_file):
        from bomshell.fetch_gis import SHAPEFILE_EXTENSIONS
        from bomshell.fetch_gis import bom_source
        from bomshell.fetch_gis import fetch_spatial_data

        fetch_spatial_data()
        expected_calls = len(bom_source) * len(SHAPEFILE_EXTENSIONS)
        assert mock_get_file.call_count == expected_calls
