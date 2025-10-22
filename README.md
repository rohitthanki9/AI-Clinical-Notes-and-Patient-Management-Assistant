# AI Clinical Notes and Patient Management Assistant

A standalone, offline desktop application for doctors and clinicians to generate AI-powered clinical notes and manage patient records securely.

## Features

- **Doctor Authentication**: Secure login/signup system with encrypted credentials
- **Voice Recording & Transcription**: Record consultations or upload audio files with offline Whisper transcription
- **AI Note Generation**: Generate structured SOAP, Referral, and Discharge notes using local Llama 3 (via Ollama)
- **ICD-10 Codes**: Automatic suggestion and management of diagnostic codes
- **Patient Management**: Full CRUD operations for patient records with search functionality
- **Secure Storage**: AES-256 encryption for sensitive data
- **Export Options**: Export notes to PDF or DOCX with professional formatting
- **100% Offline**: Works completely offline once models are installed

## Tech Stack

| Feature | Technology |
|---------|-----------|
| GUI | Tkinter + ttkbootstrap |
| Database | SQLite3 |
| Authentication | SHA-256 hashing |
| Speech-to-Text | OpenAI Whisper |
| LLM | Ollama (Llama 3) |
| Encryption | AES-256 (Fernet) |
| Export | python-docx, reportlab |
| Audio | sounddevice, soundfile |

## Project Structure

```
AI-Clinical-Notes-and-Patient-Management-Assistant/
│
├── main.py                           # Application entry point
├── modules/
│   ├── __init__.py
│   ├── config_manager.py            # Configuration management
│   ├── encryption_manager.py        # AES-256 encryption
│   ├── patient_db.py                # SQLite database operations
│   ├── icd_lookup.py                # ICD-10 code dictionary
│   ├── speech_to_text.py            # Whisper integration
│   ├── llm_processing_ollama.py     # Ollama/Llama 3 integration
│   ├── note_formatter.py            # Note formatting utilities
│   ├── export_manager.py            # PDF/DOCX export
│   ├── gui_login.py                 # Login/signup interface
│   └── gui_dashboard.py             # Main dashboard interface
├── prompts/
│   ├── soap_template.txt            # SOAP note template
│   ├── referral_template.txt        # Referral note template
│   └── discharge_template.txt       # Discharge summary template
├── data/
│   ├── patients.db                  # SQLite database (auto-created)
│   ├── .encryption.key              # Encryption key (auto-created)
│   └── config.json                  # Configuration file (auto-created)
├── assets/                          # Logo and UI assets (optional)
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Installation

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Ollama** (for AI features)
   - Download from: https://ollama.ai
   - Install and start Ollama
   - Pull Llama 3 model:
     ```bash
     ollama pull llama3
     ```

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd AI-Clinical-Notes-and-Patient-Management-Assistant
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Activate on Windows:
   venv\Scripts\activate

   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## First-Time Setup

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Create a doctor account**
   - Click the "Sign Up" tab
   - Fill in your name, email, and password
   - Click "Create Account"

3. **Log in**
   - Enter your email and password
   - Click "Login"

## Usage Guide

### Managing Patients

1. **Add a Patient**
   - Go to the "Patients" tab
   - Click "Add Patient"
   - Fill in patient details
   - Click "Save"

2. **Search Patients**
   - Use the search bar to find patients by name, diagnosis, or ICD code

3. **Edit/Delete Patients**
   - Select a patient from the list
   - Click "Edit Patient" or "Delete Patient"

### Generating Clinical Notes

1. **Select a Patient**
   - Go to the "Patients" tab
   - Double-click on a patient (or select and click "Select for Notes")

2. **Input Consultation Data**

   **Option A: Record Voice**
   - Click "Start Recording"
   - Speak your consultation notes
   - Click "Stop Recording"
   - Wait for automatic transcription

   **Option B: Upload Audio File**
   - Click "Upload Audio"
   - Select a WAV, MP3, or M4A file
   - Wait for automatic transcription

   **Option C: Type Directly**
   - Type or paste consultation notes into the text area

3. **Generate Note**
   - Select note type (SOAP, Referral, or Discharge)
   - Click "Generate Clinical Note"
   - Wait for AI to generate the structured note
   - Review the generated note and ICD code suggestions

4. **Save or Export**
   - Click "Save to Database" to store in patient record
   - Click "Export PDF" or "Export DOCX" to save to file

### ICD-10 Codes

The application includes a built-in ICD-10 code dictionary with common diagnoses:

- Automatically suggests codes based on note content
- View suggestions in the ICD-10 panel
- Codes are saved with patient records and notes

### Settings

- Check Ollama connection status
- View system information
- Check database statistics

## Configuration

Edit `data/config.json` to customize:

```json
{
    "ollama_url": "http://localhost:11434",
    "ollama_model": "llama3",
    "whisper_model": "base",
    "clinic_name": "Your Clinic Name",
    "theme": "flatly"
}
```

### Whisper Model Options

- `tiny`: Fastest, least accurate (~1GB)
- `base`: Good balance (~1GB) **[Default]**
- `small`: Better accuracy (~2GB)
- `medium`: High accuracy (~5GB)
- `large`: Best accuracy (~10GB)

## Security Features

- **Password Hashing**: SHA-256 for doctor credentials
- **Data Encryption**: AES-256 (Fernet) for sensitive data
- **Local Storage**: All data stored locally, never transmitted
- **Secure Keys**: Encryption keys stored with restrictive permissions

## Building Standalone Executable

Create a standalone .exe file (Windows):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Clinical Notes AI" main.py
```

The executable will be in the `dist/` folder.

## Troubleshooting

### Ollama Not Connected

**Problem**: "Ollama: Not Connected" message

**Solution**:
1. Ensure Ollama is installed and running
2. Check that Llama 3 is installed: `ollama list`
3. If not, install it: `ollama pull llama3`
4. Verify URL in config: `http://localhost:11434`

### Audio Recording Issues

**Problem**: Recording button doesn't work

**Solution**:
1. Check microphone permissions
2. Test microphone in system settings
3. Try selecting a different audio device

### Whisper Model Download

**Problem**: First transcription is slow

**Solution**:
- Whisper automatically downloads the model on first use
- Subsequent uses will be much faster
- Use a smaller model for faster processing

### Database Locked

**Problem**: "Database is locked" error

**Solution**:
- Close other instances of the application
- Restart the application

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 5GB free space for models
- **CPU**: Multi-core processor recommended for AI features

## Contributing

This is a standalone medical documentation tool. For feature requests or bug reports, please contact the development team.

## License

This software is for medical documentation purposes only. Ensure compliance with local healthcare regulations (HIPAA, GDPR, etc.) when using this application.

## Disclaimer

This application is designed to assist healthcare professionals in documentation. All AI-generated notes should be reviewed and validated by a qualified medical professional before use in patient care. The software does not provide medical advice, diagnosis, or treatment recommendations.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify Ollama is running and models are installed

---

**Version**: 1.0
**Last Updated**: 2025

Built with Python, Tkinter, Whisper, and Llama 3
