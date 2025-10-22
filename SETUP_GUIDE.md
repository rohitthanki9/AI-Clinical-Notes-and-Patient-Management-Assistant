# Quick Setup Guide

## Step 1: Install Python

Download and install Python 3.8 or higher from: https://www.python.org/downloads/

Verify installation:
```bash
python --version
```

## Step 2: Install Ollama

1. Download Ollama from: https://ollama.ai
2. Install Ollama for your operating system
3. Start Ollama (it usually starts automatically)

## Step 3: Install Llama 3 Model

Open a terminal/command prompt and run:
```bash
ollama pull llama3
```

This will download the Llama 3 model (about 4.7 GB). This only needs to be done once.

Verify the model is installed:
```bash
ollama list
```

## Step 4: Set Up the Application

1. Open a terminal/command prompt
2. Navigate to the application folder:
   ```bash
   cd AI-Clinical-Notes-and-Patient-Management-Assistant
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

5. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Step 5: Run the Application

```bash
python main.py
```

## First-Time Use

1. The application will create necessary folders and files automatically
2. Click "Sign Up" to create your doctor account
3. Log in with your credentials
4. Start managing patients and generating notes!

## Troubleshooting

### "Ollama not connected" message

Make sure Ollama is running:
- **Windows**: Check if Ollama is running in the system tray
- **macOS**: Check if Ollama app is running
- **Linux**: Run `ollama serve` in a terminal

### "Module not found" errors

Make sure you activated the virtual environment and installed all requirements:
```bash
pip install -r requirements.txt
```

### Whisper model download

The first time you use speech-to-text, Whisper will download its model (about 1 GB for the base model). This is normal and only happens once.

### Slow AI generation

- Ensure you have a decent CPU (multi-core recommended)
- Close other heavy applications
- Consider using a smaller Whisper model in settings

## Optional: Whisper Model Selection

Edit `data/config.json` and change the `whisper_model` value:

- `tiny` - Fastest, least accurate (~1GB)
- `base` - Good balance (~1GB) [Default]
- `small` - Better accuracy (~2GB)
- `medium` - High accuracy (~5GB)
- `large` - Best accuracy (~10GB)

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 20.04+
- **RAM**: 8GB recommended (4GB minimum)
- **Storage**: 10GB free space
- **CPU**: Multi-core processor recommended

## Need Help?

Refer to the main README.md for detailed documentation and troubleshooting.

---

**Happy documenting!**
