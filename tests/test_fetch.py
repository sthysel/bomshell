from unittest.mock import MagicMock
from unittest.mock import patch

from bomshell.fetch import remove_existing_file


class TestRemoveExistingFile:
    def test_file_does_not_exist(self, tmp_path):
        result = remove_existing_file(str(tmp_path / "nope.dbf"), overwrite=False)
        assert result is True

    def test_file_exists_no_overwrite(self, tmp_path):
        f = tmp_path / "existing.dbf"
        f.write_text("data")
        result = remove_existing_file(str(f), overwrite=False)
        assert result is False
        assert f.exists()

    def test_file_exists_with_overwrite(self, tmp_path):
        f = tmp_path / "existing.dbf"
        f.write_text("data")
        result = remove_existing_file(str(f), overwrite=True)
        assert result is True
        assert not f.exists()


class TestGetFile:
    @patch("bomshell.fetch.ftputil")
    def test_skips_existing_file_no_overwrite(self, mock_ftputil, tmp_path):
        from bomshell import settings
        from bomshell.fetch import get_file

        old_cache = settings.SPATIAL_CACHE
        old_overwrite = settings.OVERWRITE
        try:
            settings.SPATIAL_CACHE = str(tmp_path)
            settings.OVERWRITE = False

            target = tmp_path / "test.dbf"
            target.write_text("existing")

            result = get_file("/some/dir", "test.dbf", "ftp.example.com")
            assert result is True
            mock_ftputil.FTPHost.assert_not_called()
        finally:
            settings.SPATIAL_CACHE = old_cache
            settings.OVERWRITE = old_overwrite

    @patch("bomshell.fetch.ftputil")
    def test_downloads_new_file(self, mock_ftputil, tmp_path):
        from bomshell import settings
        from bomshell.fetch import get_file

        old_cache = settings.SPATIAL_CACHE
        old_overwrite = settings.OVERWRITE
        try:
            settings.SPATIAL_CACHE = str(tmp_path)
            settings.OVERWRITE = False

            mock_host = MagicMock()
            mock_host.path.exists.return_value = True
            mock_ftputil.FTPHost.return_value.__enter__ = MagicMock(return_value=mock_host)
            mock_ftputil.FTPHost.return_value.__exit__ = MagicMock(return_value=False)

            result = get_file("/some/dir", "new.dbf", "ftp.example.com")
            assert result is True
        finally:
            settings.SPATIAL_CACHE = old_cache
            settings.OVERWRITE = old_overwrite
