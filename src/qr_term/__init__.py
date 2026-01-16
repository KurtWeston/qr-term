"""QR code generator for terminal."""

__version__ = "0.1.0"
__author__ = "QR-Term Contributors"

from qr_term.generator import QRGenerator
from qr_term.wifi import WiFiQR

__all__ = ["QRGenerator", "WiFiQR"]
