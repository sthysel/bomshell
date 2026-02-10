from unittest.mock import patch

from typer.testing import CliRunner

from bomshell.cli import app


class TestSpatialFetch:
    @patch("bomshell.fetch_gis.fetch_spatial_data")
    def test_fetch(self, mock_fetch):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "fetch"])
        assert result.exit_code == 0
        mock_fetch.assert_called_once()

    @patch("bomshell.fetch_gis.fetch_spatial_data")
    def test_sync_sets_overwrite(self, mock_fetch):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "sync"])
        assert result.exit_code == 0
        mock_fetch.assert_called_once()

    @patch("bomshell.fetch_gis.create_spatial_database")
    def test_build(self, mock_build):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "build"])
        assert result.exit_code == 0
        mock_build.assert_called_once()


class TestSpatialCsvdump:
    def test_no_spatial_type_shows_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "csvdump"])
        assert "Select one of the spatial types" in result.output

    @patch("bomshell.dump_gis.dump_to_csv")
    def test_with_type(self, mock_dump):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "csvdump", "-s", "forecast_districts"])
        assert result.exit_code == 0
        mock_dump.assert_called_once_with("forecast_districts")


class TestSpatialTabledump:
    def test_no_spatial_type_shows_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "tabledump"])
        assert "Select one of the spatial types" in result.output

    @patch("bomshell.dump_gis.dump_to_table")
    def test_with_type(self, mock_dump):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "tabledump", "-s", "forecast_districts"])
        assert result.exit_code == 0
        mock_dump.assert_called_once_with("forecast_districts")


class TestSpatialMap:
    def test_no_type_shows_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "map"])
        assert "Select one or more spatial types" in result.output

    @patch("bomshell.visualize.open_in_browser")
    @patch("bomshell.visualize.create_map", return_value="/tmp/test.html")
    def test_with_type(self, mock_create, mock_open):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "map", "-s", "radar_location"])
        assert result.exit_code == 0
        assert "Map saved to" in result.output

    @patch("bomshell.visualize.create_map", side_effect=FileNotFoundError("not found"))
    def test_missing_data_shows_error(self, mock_create):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "map", "-s", "radar_location"])
        assert result.exit_code == 1
        assert "not found" in result.output

    @patch("bomshell.visualize.open_in_browser")
    @patch("bomshell.visualize.create_map", return_value="/tmp/test.html")
    def test_no_open_flag(self, mock_create, mock_open):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "map", "-s", "radar_location", "--no-open"])
        assert result.exit_code == 0
        mock_open.assert_not_called()

    @patch("bomshell.visualize.open_in_browser")
    @patch("bomshell.visualize.create_map", return_value="/tmp/test.html")
    def test_multiple_layers_shows_tip(self, mock_create, mock_open):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "map", "-s", "radar_location", "-s", "forecast_districts"])
        assert result.exit_code == 0
        assert "layer control" in result.output


class TestSpatialHelp:
    def test_spatial_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["spatial", "--help"])
        assert result.exit_code == 0
        assert "Spatial database management" in result.output
