"""Tests for WiFi QR code generation."""

import pytest
from qr_term.wifi import WiFiQR


class TestWiFiQR:
    def test_generate_wpa_network(self):
        wifi = WiFiQR("MyNetwork", "password123", "WPA")
        result = wifi.generate()
        assert result.startswith("WIFI:")
        assert "T:WPA;" in result
        assert "S:MyNetwork;" in result
        assert "P:password123;" in result
    
    def test_generate_nopass_network(self):
        wifi = WiFiQR("OpenNetwork", security="nopass")
        result = wifi.generate()
        assert "T:nopass;" in result
        assert "S:OpenNetwork;" in result
        assert "P:" not in result
    
    def test_empty_ssid_raises_error(self):
        with pytest.raises(ValueError, match="SSID cannot be empty"):
            WiFiQR("", "password")
    
    def test_invalid_security_raises_error(self):
        with pytest.raises(ValueError, match="Security must be one of"):
            WiFiQR("Network", "pass", "INVALID")
    
    def test_wpa_without_password_raises_error(self):
        with pytest.raises(ValueError, match="Password required"):
            WiFiQR("Network", "", "WPA")
    
    def test_hidden_network(self):
        wifi = WiFiQR("HiddenNet", "secret", "WPA", hidden=True)
        result = wifi.generate()
        assert "H:true;" in result
    
    def test_escape_special_characters(self):
        wifi = WiFiQR("Net;work", "pass\\word", "WPA")
        result = wifi.generate()
        assert "S:Net\\;work;" in result
        assert "P:pass\\\\word;" in result
    
    def test_from_string_parsing(self):
        wifi_string = "WIFI:T:WPA;S:TestNet;P:testpass;;"
        wifi = WiFiQR.from_string(wifi_string)
        assert wifi.ssid == "TestNet"
        assert wifi.password == "testpass"
        assert wifi.security == "WPA"
        assert wifi.hidden is False
    
    def test_from_string_invalid_format(self):
        with pytest.raises(ValueError, match="Invalid WiFi QR format"):
            WiFiQR.from_string("INVALID:T:WPA;")
    
    def test_from_string_with_hidden(self):
        wifi_string = "WIFI:T:WPA;S:Hidden;P:pass;H:true;;"
        wifi = WiFiQR.from_string(wifi_string)
        assert wifi.hidden is True