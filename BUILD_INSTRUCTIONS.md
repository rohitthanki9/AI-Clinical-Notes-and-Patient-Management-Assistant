# PyInstaller Build Script for Clinical Notes AI

## Quick Build Commands

### For Windows (.exe with icon):

```bash
# If you have icon.ico file:
pyinstaller --onefile --windowed --name "Clinical Notes AI" --icon=assets/icon.ico main.py

# If you only have icon.png, first convert it:
# Install pillow if not already installed
pip install pillow

# Then use the build script below
python build.py
```

### For macOS (.app with icon):

```bash
pyinstaller --onefile --windowed --name "Clinical Notes AI" --icon=assets/icon.icns main.py
```

### For Linux:

```bash
pyinstaller --onefile --windowed --name "Clinical Notes AI" main.py
```

## Convert PNG to ICO (Windows)

Use this Python script to convert icon.png to icon.ico:

```python
from PIL import Image

# Open the PNG file
img = Image.open('assets/icon.png')

# Save as ICO (multiple sizes for Windows)
img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
```

## Complete Build with Dependencies

### Option 1: Using Modified Command

```bash
pyinstaller --onefile --windowed \
  --name "Clinical Notes AI" \
  --icon=assets/icon.ico \
  --add-data "prompts;prompts" \
  --add-data "assets;assets" \
  --hidden-import=whisper \
  --hidden-import=ttkbootstrap \
  --hidden-import=sounddevice \
  --hidden-import=soundfile \
  main.py
```

**For Windows PowerShell, use:**
```powershell
pyinstaller --onefile --windowed --name "Clinical Notes AI" --icon=assets/icon.ico --add-data "prompts;prompts" --add-data "assets;assets" --hidden-import=whisper --hidden-import=ttkbootstrap --hidden-import=sounddevice --hidden-import=soundfile main.py
```

### Option 2: Using .spec File (Recommended)

Use the provided `Clinical_Notes_AI.spec` file:

```bash
pyinstaller Clinical_Notes_AI.spec
```

## After Building

Your executable will be in:
- `dist/Clinical Notes AI.exe` (Windows)
- `dist/Clinical Notes AI.app` (macOS)
- `dist/Clinical Notes AI` (Linux)

## Notes

1. **Icon Requirements:**
   - Windows: `.ico` format (use conversion script above)
   - macOS: `.icns` format
   - Linux: Icon not embedded in executable

2. **Data Files:**
   - `prompts/` folder is included
   - `assets/` folder is included
   - Database will be created on first run

3. **Size:**
   - Expect ~500MB-1GB due to Whisper and other ML dependencies
   - First build takes 5-10 minutes

4. **Testing:**
   - Test the executable on a clean machine without Python
   - Ensure Ollama is installed separately

## Troubleshooting

### Missing modules error:
```bash
# Add missing modules with --hidden-import
pyinstaller ... --hidden-import=module_name
```

### Icon not showing:
- Ensure icon.ico is in the correct format
- Windows may cache icons - try renaming the exe
- Right-click exe → Properties to verify icon

### Large file size:
- This is normal for ML applications
- Use --onefile for single executable
- Use --onedir for faster startup (multiple files)
