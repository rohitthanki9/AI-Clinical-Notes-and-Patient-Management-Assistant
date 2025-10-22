# Quick Start Guide

## Get Started in 5 Minutes!

### Step 1: Install Ollama (3 minutes)

1. Visit https://ollama.ai and download for your OS
2. Install and start Ollama
3. Open terminal and run:
   ```bash
   ollama pull llama3
   ```

### Step 2: Install Python Dependencies (2 minutes)

```bash
# Navigate to project folder
cd AI-Clinical-Notes-and-Patient-Management-Assistant

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python main.py
```

### Step 4: Create Your Account

1. Click "Sign Up" tab
2. Enter your name, email, and password
3. Click "Create Account"
4. Log in with your credentials

## Your First Clinical Note

1. **Add a Patient**
   - Go to "Patients" tab
   - Click "Add Patient"
   - Fill in details and save

2. **Create a Note**
   - Double-click the patient
   - Choose recording method:
     - Click "Start Recording" to record voice
     - OR click "Upload Audio" for a file
     - OR type consultation notes directly

3. **Generate Note**
   - Select note type (SOAP/Referral/Discharge)
   - Click "Generate Clinical Note"
   - Review the AI-generated note

4. **Save & Export**
   - Click "Save to Database"
   - OR "Export PDF" / "Export DOCX"

## System Requirements

- Python 3.8+
- 8GB RAM (4GB minimum)
- 10GB free disk space
- Internet only for initial setup

## Need Help?

- See README.md for detailed documentation
- See SETUP_GUIDE.md for troubleshooting
- See PROJECT_SUMMARY.md for technical details

---

That's it! Start documenting efficiently with AI assistance.
