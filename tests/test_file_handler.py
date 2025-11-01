"""Unit tests for intersector.utils.file_handler."""

from unittest.mock import MagicMock, patch

from intersector.utils import file_handler


class TestExportStep:
    """Tests for the export_step function."""

    @staticmethod
    @patch("intersector.utils.file_handler.STEPControl_Writer")
    def test_export_step_success(mock_writer_class):
        """Test successful STEP export."""
        mock_writer = MagicMock()
        mock_writer.Write.return_value = file_handler.IFSelect_RetDone
        mock_writer_class.return_value = mock_writer

        mock_shape = MagicMock()
        result = file_handler.export_step(mock_shape, "ok.step")

        assert result is True
        mock_writer.Transfer.assert_called_once_with(
            mock_shape, file_handler.STEPControl_AsIs
        )
        mock_writer.Write.assert_called_once_with("ok.step")

    @staticmethod
    @patch("intersector.utils.file_handler.STEPControl_Writer")
    def test_export_step_failure_status(mock_writer_class):
        """Test export_step returns False when status is not RetDone."""
        mock_writer = MagicMock()
        mock_writer.Write.return_value = 999  # Not IFSelect_RetDone
        mock_writer_class.return_value = mock_writer

        mock_shape = MagicMock()
        result = file_handler.export_step(mock_shape, "bad.step")

        assert result is False

    @staticmethod
    @patch(
        "intersector.utils.file_handler.STEPControl_Writer",
        side_effect=OSError("Disk full"),
    )
    def test_export_step_exception(_):
        """Test export_step handles exceptions gracefully."""
        mock_shape = MagicMock()
        result = file_handler.export_step(mock_shape, "fail.step")

        assert result is False


class TestReadStep:
    """Tests for the read_step function."""

    @staticmethod
    @patch("intersector.utils.file_handler.os.path.exists", return_value=True)
    @patch("intersector.utils.file_handler.STEPControl_Reader")
    def test_read_step_success(mock_reader_class, _mock_exists):
        """Test successful reading of a STEP file."""
        mock_reader = MagicMock()
        mock_reader.ReadFile.return_value = file_handler.IFSelect_RetDone
        mock_shape = MagicMock()
        mock_shape.IsNull.return_value = False
        mock_reader.OneShape.return_value = mock_shape
        mock_reader_class.return_value = mock_reader

        result = file_handler.read_step("ok.step")

        assert result == mock_shape
        mock_reader.ReadFile.assert_called_once_with("ok.step")

    @staticmethod
    @patch("intersector.utils.file_handler.os.path.exists", return_value=True)
    @patch("intersector.utils.file_handler.STEPControl_Reader")
    def test_read_step_failure_status(mock_reader_class, _mock_exists):
        """Test read_step returns None when ReadFile status is bad."""
        mock_reader = MagicMock()
        mock_reader.ReadFile.return_value = 999
        mock_reader_class.return_value = mock_reader

        result = file_handler.read_step("bad.step")

        assert result is None

    @staticmethod
    @patch("intersector.utils.file_handler.os.path.exists", return_value=True)
    @patch("intersector.utils.file_handler.STEPControl_Reader")
    def test_read_step_null_shape(mock_reader_class, _mock_exists):
        """Test read_step returns None if OneShape is null."""
        mock_reader = MagicMock()
        mock_reader.ReadFile.return_value = file_handler.IFSelect_RetDone
        mock_shape = MagicMock()
        mock_shape.IsNull.return_value = True
        mock_reader.OneShape.return_value = mock_shape
        mock_reader_class.return_value = mock_reader

        result = file_handler.read_step("empty.step")

        assert result is None

    @staticmethod
    @patch("intersector.utils.file_handler.os.path.exists", return_value=False)
    def test_read_step_file_not_found(_mock_exists):
        """Test read_step returns None if file does not exist."""
        result = file_handler.read_step("missing.step")
        assert result is None

    @staticmethod
    @patch("intersector.utils.file_handler.os.path.exists", return_value=True)
    @patch(
        "intersector.utils.file_handler.STEPControl_Reader",
        side_effect=RuntimeError("Corrupt file"),
    )
    def test_read_step_exception(_mock_reader, _mock_exists):
        """Test read_step handles exceptions gracefully."""
        result = file_handler.read_step("crash.step")
        assert result is None
