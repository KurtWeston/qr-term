# qr-term

Generate QR codes in your terminal for quick sharing of URLs, WiFi credentials, and text

## Features

- Generate QR codes rendered as ASCII/Unicode blocks in terminal
- Support for plain text, URLs, and WiFi credentials
- WiFi QR code generation with SSID, password, and encryption type (WPA/WEP/nopass)
- Adjustable QR code size with --size flag for different terminal dimensions
- Inverted color mode (--invert) for light terminal backgrounds
- Border control (--border) to add/remove quiet zone around QR code
- Output to file option (--output) for saving QR as text file
- Automatic error correction level selection based on data length
- Pipe support for reading input from stdin
- Colorized output with optional --no-color flag for plain text

## How to Use

Use this project when you need to:

- Quickly solve problems related to qr-term
- Integrate python functionality into your workflow
- Learn how python handles common patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/qr-term.git
cd qr-term

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Dependencies

- `qrcode`
- `pytest`
- `pytest-cov`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
