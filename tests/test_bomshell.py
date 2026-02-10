from typer.testing import CliRunner

from bomshell.cli import app


def test_main_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Retrieve weather data from the Australian Bureau of Meteorology" in result.output


def test_knobs():
    runner = CliRunner()
    result = runner.invoke(app, ["knobs"])

    assert result.exit_code == 0
    assert "BOM_CACHE" in result.output


def test_json_knobs():
    import json

    runner = CliRunner()
    result = runner.invoke(app, ["--json", "knobs"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "BOM_CACHE" in data
