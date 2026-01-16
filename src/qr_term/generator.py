"""QR code generation and terminal rendering."""

import qrcode
from qrcode.image.base import BaseImage
from typing import List


class QRGenerator:
    def __init__(self, size: int = 1, border: int = 2, invert: bool = False, use_color: bool = True):
        self.size = max(1, size)
        self.border = max(0, border)
        self.invert = invert
        self.use_color = use_color
        self.block_char = "\u2588\u2588"
        self.empty_char = "  "
    
    def _get_error_correction(self, data: str) -> int:
        data_len = len(data)
        if data_len < 50:
            return qrcode.constants.ERROR_CORRECT_H
        elif data_len < 100:
            return qrcode.constants.ERROR_CORRECT_Q
        elif data_len < 200:
            return qrcode.constants.ERROR_CORRECT_M
        return qrcode.constants.ERROR_CORRECT_L
    
    def _create_qr(self, data: str) -> qrcode.QRCode:
        qr = qrcode.QRCode(
            version=None,
            error_correction=self._get_error_correction(data),
            box_size=self.size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr
    
    def _get_color_codes(self) -> tuple:
        if not self.use_color:
            return "", ""
        
        if self.invert:
            return "\033[97m", "\033[0m"
        return "\033[40m\033[97m", "\033[0m"
    
    def _render_terminal(self, matrix: List[List[bool]]) -> str:
        start_color, end_color = self._get_color_codes()
        lines = []
        
        for row in matrix:
            line = start_color
            for cell in row:
                if self.invert:
                    line += self.empty_char if cell else self.block_char
                else:
                    line += self.block_char if cell else self.empty_char
            line += end_color
            lines.append(line)
        
        return "\n".join(lines)
    
    def generate(self, data: str) -> str:
        if not data:
            raise ValueError("Data cannot be empty")
        
        qr = self._create_qr(data)
        matrix = qr.get_matrix()
        return self._render_terminal(matrix)
