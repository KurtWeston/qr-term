"""WiFi QR code format generator."""

from typing import Optional


class WiFiQR:
    VALID_SECURITY = {"WPA", "WEP", "nopass"}
    
    def __init__(self, ssid: str, password: str = "", security: str = "WPA", hidden: bool = False):
        if not ssid:
            raise ValueError("SSID cannot be empty")
        
        if security not in self.VALID_SECURITY:
            raise ValueError(f"Security must be one of {self.VALID_SECURITY}")
        
        if security != "nopass" and not password:
            raise ValueError(f"Password required for {security} security")
        
        self.ssid = ssid
        self.password = password
        self.security = security
        self.hidden = hidden
    
    @staticmethod
    def _escape(text: str) -> str:
        special_chars = ["\\", ";", ",", ":", '"']
        for char in special_chars:
            text = text.replace(char, f"\\{char}")
        return text
    
    def generate(self) -> str:
        parts = ["WIFI:"]
        parts.append(f"T:{self.security};")
        parts.append(f"S:{self._escape(self.ssid)};")
        
        if self.security != "nopass":
            parts.append(f"P:{self._escape(self.password)};")
        
        if self.hidden:
            parts.append("H:true;")
        
        parts.append(";")
        return "".join(parts)
    
    @classmethod
    def from_string(cls, wifi_string: str) -> "WiFiQR":
        if not wifi_string.startswith("WIFI:"):
            raise ValueError("Invalid WiFi QR format")
        
        params = {}
        parts = wifi_string[5:].split(";")
        
        for part in parts:
            if ":" in part:
                key, value = part.split(":", 1)
                params[key] = value.replace("\\;", ";").replace("\\\\", "\\")
        
        ssid = params.get("S", "")
        password = params.get("P", "")
        security = params.get("T", "WPA")
        hidden = params.get("H", "").lower() == "true"
        
        return cls(ssid, password, security, hidden)
