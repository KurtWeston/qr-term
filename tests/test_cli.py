"""Tests for CLI interface."""

import pytest
from io import StringIO
from unittest.mock import patch, mock_open
from qr_term.cli import create_parser, main, read_stdin


class TestCLI:
    def test_parser_creation(self):
        parser = create_parser()
        assert parser.prog == "qr-term"
    
    def test_parse_basic_args(self):
        parser = create_parser()
        args = parser.parse_args(["test data"])
        assert args.data == "test data"
        assert args.size == 1
        assert args.border == 2
    
    def test_parse_wifi_args(self):
        parser = create_parser()
        args = parser.parse_args(["--wifi", "--ssid", "MyNet", "--password", "pass"])
        assert args.wifi is True
        assert args.ssid == "MyNet"
        assert args.password == "pass"
    
    @patch('sys.stdin', StringIO("piped data"))
    @patch('sys.stdin.isatty', return_value=False)
    def test_read_stdin(self, mock_isatty):
        result = read_stdin()
        assert result == "piped data"
    
    @patch('sys.stdin.isatty', return_value=True)
    def test_read_stdin_no_pipe(self, mock_isatty):
        result = read_stdin()
        assert result is None
    
    @patch('sys.argv', ['qr-term', 'test'])
    @patch('builtins.print')
    def test_main_success(self, mock_print):
        result = main()
        assert result == 0
        assert mock_print.called
    
    @patch('sys.argv', ['qr-term', '--wifi', '--ssid', 'Net', '--password', 'pass'])
    @patch('builtins.print')
    def test_main_wifi_mode(self, mock_print):
        result = main()
        assert result == 0
    
    @patch('sys.argv', ['qr-term', '--wifi'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_wifi_no_ssid_error(self, mock_stderr):
        result = main()
        assert result == 1
        assert "--ssid is required" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['qr-term'])
    @patch('sys.stdin.isatty', return_value=True)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_no_data_error(self, mock_stderr, mock_isatty):
        result = main()
        assert result == 1
        assert "No data provided" in mock_stderr.getvalue()
    
    @patch('sys.argv', ['qr-term', 'test', '--output', 'out.txt'])
    @patch('builtins.open', mock_open())
    @patch('builtins.print')
    def test_main_output_file(self, mock_print, mock_file):
        result = main()
        assert result == 0
        mock_file.assert_called_once_with('out.txt', 'w', encoding='utf-8')