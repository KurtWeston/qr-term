#!/usr/bin/env python3
"""CLI interface for qr-term."""

import argparse
import sys
from typing import Optional

from qr_term import __version__
from qr_term.generator import QRGenerator
from qr_term.wifi import WiFiQR


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qr-term",
        description="Generate QR codes in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("data", nargs="?", help="Data to encode (URL, text, etc.)")
    parser.add_argument("-s", "--size", type=int, default=1, help="QR code size multiplier (default: 1)")
    parser.add_argument("-i", "--invert", action="store_true", help="Invert colors for light backgrounds")
    parser.add_argument("-b", "--border", type=int, default=2, help="Border size in modules (default: 2)")
    parser.add_argument("-o", "--output", type=str, help="Save QR code to file")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    wifi_group = parser.add_argument_group("WiFi QR code options")
    wifi_group.add_argument("--wifi", action="store_true", help="Generate WiFi QR code")
    wifi_group.add_argument("--ssid", type=str, help="WiFi SSID")
    wifi_group.add_argument("--password", type=str, help="WiFi password")
    wifi_group.add_argument(
        "--security",
        type=str,
        choices=["WPA", "WEP", "nopass"],
        default="WPA",
        help="WiFi security type (default: WPA)"
    )
    wifi_group.add_argument("--hidden", action="store_true", help="Hidden SSID")
    
    return parser


def read_stdin() -> Optional[str]:
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    
    data = args.data or read_stdin()
    
    if args.wifi:
        if not args.ssid:
            print("Error: --ssid is required for WiFi QR codes", file=sys.stderr)
            return 1
        wifi_qr = WiFiQR(args.ssid, args.password or "", args.security, args.hidden)
        data = wifi_qr.generate()
    elif not data:
        print("Error: No data provided. Use positional argument or pipe data via stdin.", file=sys.stderr)
        parser.print_help()
        return 1
    
    try:
        generator = QRGenerator(
            size=args.size,
            border=args.border,
            invert=args.invert,
            use_color=not args.no_color
        )
        qr_output = generator.generate(data)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(qr_output)
            print(f"QR code saved to {args.output}")
        else:
            print(qr_output)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
