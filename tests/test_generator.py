"""Tests for QR code generator."""

import pytest
from qr_term.generator import QRGenerator


class TestQRGenerator:
    def test_generate_simple_text(self):
        generator = QRGenerator()
        result = generator.generate("Hello World")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "\n" in result
    
    def test_generate_empty_data_raises_error(self):
        generator = QRGenerator()
        with pytest.raises(ValueError, match="Data cannot be empty"):
            generator.generate("")
    
    def test_size_multiplier(self):
        gen_small = QRGenerator(size=1)
        gen_large = QRGenerator(size=3)
        result_small = gen_small.generate("test")
        result_large = gen_large.generate("test")
        assert len(result_large) >= len(result_small)
    
    def test_border_control(self):
        gen_no_border = QRGenerator(border=0)
        gen_large_border = QRGenerator(border=5)
        result_no = gen_no_border.generate("test")
        result_large = gen_large_border.generate("test")
        assert len(result_large.split("\n")) > len(result_no.split("\n"))
    
    def test_invert_mode(self):
        gen_normal = QRGenerator(invert=False)
        gen_inverted = QRGenerator(invert=True)
        result_normal = gen_normal.generate("test")
        result_inverted = gen_inverted.generate("test")
        assert result_normal != result_inverted
    
    def test_no_color_mode(self):
        gen_color = QRGenerator(use_color=True)
        gen_no_color = QRGenerator(use_color=False)
        result_color = gen_color.generate("test")
        result_no_color = gen_no_color.generate("test")
        assert "\033[" in result_color
        assert "\033[" not in result_no_color
    
    def test_error_correction_levels(self):
        generator = QRGenerator()
        short_data = "hi"
        medium_data = "a" * 75
        long_data = "a" * 150
        very_long_data = "a" * 250
        
        assert generator._get_error_correction(short_data) == 3
        assert generator._get_error_correction(medium_data) == 2
        assert generator._get_error_correction(long_data) == 1
        assert generator._get_error_correction(very_long_data) == 0
    
    def test_negative_size_normalized(self):
        generator = QRGenerator(size=-5)
        assert generator.size == 1
    
    def test_negative_border_normalized(self):
        generator = QRGenerator(border=-3)
        assert generator.border == 0