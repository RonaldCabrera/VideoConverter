# Video Converter

A simple and fast desktop application to batch convert WebM videos to MP4 format with GPU acceleration support.

## Features

- 🚀 **GPU Acceleration** - Support for NVIDIA, AMD, and Intel hardware encoding
- 📦 **Batch Processing** - Convert multiple files at once
- 🎯 **Simple Interface** - Easy-to-use GUI built with PySide6
- ⚡ **Fast Conversion** - Hardware acceleration makes conversions significantly faster
- 🔄 **Auto Cleanup** - Automatically removes source files after successful conversion
- 💾 **Automatic Scaling** - Ensures output videos have dimensions divisible by 2

## Supported Encoders

- **CPU (libx264)** - Default software encoding, works on all systems
- **NVIDIA GPU (h264_nvenc)** - For NVIDIA graphics cards with NVENC support
- **AMD GPU (h264_amf)** - For AMD graphics cards with AMF support
- **Intel GPU (h264_qsv)** - For Intel integrated graphics with Quick Sync Video

## Requirements

- Python 3.7 or higher
- FFmpeg installed and added to system PATH
- PySide6

### Installing FFmpeg

**Windows:**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the files
3. Add the `bin` folder to your system PATH

**Linux:**
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
sudo dnf install ffmpeg  # Fedora
```

**macOS:**
```bash
brew install ffmpeg
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/webm-to-mp4-converter.git
cd webm-to-mp4-converter
```

2. Install required Python packages:
```bash
pip install PySide6
```

3. Run the application:
```bash
python webm_converter.py
```

## Usage

1. **Launch the application**
2. **Select your encoder** from the dropdown menu:
   - Choose GPU encoding if you have a compatible graphics card
   - Use CPU encoding if unsure or if GPU encoding fails
3. **Place your `.webm` files** in the `Input` folder (created automatically)
4. **Click "Start"** to begin conversion
5. **Find converted files** in the `Output` folder

### Folder Structure
```
webm-to-mp4-converter/
├── webm_converter.py
├── Input/           # Place your .webm files here
└── Output/          # Converted .mp4 files appear here
```

## Building an Executable

To create a standalone executable:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "WebM_Converter" webm_converter.py
```

The executable will be in the `dist/` folder.

**Note:** Make sure `ffmpeg.exe` is either:
- In your system PATH, or
- In the same folder as the executable

## Troubleshooting

**"ffmpeg is not recognized..."**
- Make sure FFmpeg is installed and added to your system PATH

**GPU encoding fails**
- Verify you have the latest graphics drivers installed
- Try selecting a different encoder or use CPU encoding
- Check that your GPU supports hardware encoding

**"File is being used by another process"**
- The app automatically retries deletion with delays
- If files remain in Input folder, you can manually delete them after conversion

**Conversion is slow**
- Try using GPU acceleration if available
- CPU encoding is slower but works on all systems

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [PySide6](https://wiki.qt.io/Qt_for_Python)
- Video conversion powered by [FFmpeg](https://ffmpeg.org/)

---

**Developed with ❤️ for easy video conversion**
