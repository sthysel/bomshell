from bomshell.bom_paths import catalog_url
from bomshell.bom_paths import ftp_root
from bomshell.bom_paths import sources


def test_ftp_root():
    assert ftp_root.startswith("ftp://")
    assert "bom.gov.au" in ftp_root


def test_sources_all_start_with_ftp_root():
    for key, url in sources.items():
        assert url.startswith(ftp_root), f"{key} does not start with ftp_root"


def test_known_source_keys():
    expected = {"forecast", "observation", "advice", "warning", "chart", "satellite", "radar", "ash"}
    assert set(sources.keys()) == expected


def test_catalog_url():
    assert catalog_url.startswith("http")
    assert "bom.gov.au" in catalog_url
