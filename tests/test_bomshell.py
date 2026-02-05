from click.testing import CliRunner

from bomshell.cli import main


def test_main_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Retrieve weather data from the Australian Bureau of Meteorology" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "1.1.0" in result.output


def test_knobs():
    runner = CliRunner()
    result = runner.invoke(main, ["knobs"])

    assert result.exit_code == 0
    assert "BOM_CACHE" in result.output
