# Testing Guide - AI Clinical Notes Application

This guide will walk you through testing the application step-by-step.

## Prerequisites Check

Before testing, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] Ollama installed and running
- [ ] Llama 3 model downloaded
- [ ] Virtual environment created

---

## Step 1: Run Automated Installation Test

This will verify all dependencies are properly installed:

```bash
# Make sure you're in the project directory
cd AI-Clinical-Notes-and-Patient-Management-Assistant

# Activate virtual environment if not already active
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the test script
python test_installation.py
```

**Expected Output:**
```
======================================================================
        AI Clinical Notes - Installation Test
======================================================================

Testing Python version... OK (Python 3.x.x)
Testing Tkinter... OK
Testing ttkbootstrap... OK
Testing openai-whisper... OK
...
Passed: 14/14

✓ ALL TESTS PASSED!
```

If any tests fail, see the troubleshooting section below.

---

## Step 2: Start Ollama (If Not Running)

### Windows:
Ollama should start automatically. Check system tray for the Ollama icon.

### macOS:
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve
```

### Linux:
```bash
# Start Ollama
ollama serve &
```

### Verify Ollama:
```bash
# Check if Llama3 is available
ollama list

# Should show something like:
# NAME            ID              SIZE      MODIFIED
# llama3:latest   abc123...       4.7 GB    2 days ago
```

---

## Step 3: Launch the Application

```bash
python main.py
```

**Expected Output:**
```
======================================================================
        AI Clinical Notes and Patient Management Assistant
              Offline Medical Documentation System
======================================================================

Initializing AI Clinical Notes and Patient Management Assistant...
✓ Configuration loaded
✓ Database initialized
✓ Encryption manager initialized
✓ ICD-10 lookup loaded
✓ Speech-to-text ready (Whisper model: base)
✓ LLM processor ready (Model: llama3)
✓ Ollama connection: OK
✓ Note formatter ready
✓ Export manager ready

Application initialized successfully!

Starting application...
```

A login window should appear.

---

## Step 4: Test Authentication

### Test 4.1: Create a Doctor Account

1. **Click the "Sign Up" tab**
2. **Fill in the form:**
   - Name: `Dr. Test User`
   - Email: `test@clinic.com`
   - Password: `test123456`
   - Confirm Password: `test123456`
3. **Click "Create Account"**

**Expected Result:**
- Success message: "Account created successfully! You can now log in."
- Automatically switches to Login tab
- Email field pre-filled with `test@clinic.com`

### Test 4.2: Login

1. **Enter credentials:**
   - Email: `test@clinic.com`
   - Password: `test123456`
2. **Click "Login"**

**Expected Result:**
- Success message: "Welcome, Dr. Test User!"
- Login window closes
- Dashboard opens

---

## Step 5: Test Patient Management

### Test 5.1: Add a Patient

1. **Go to "Patients" tab**
2. **Click "Add Patient" button**
3. **Fill in patient information:**
   - Full Name: `John Doe`
   - Age: `45`
   - Gender: `Male`
   - Contact: `555-1234`
   - Diagnosis: `Hypertension`
   - ICD Code: `I10`
   - Notes: `Regular checkup patient`
4. **Click "Save"**

**Expected Result:**
- Success message: "Patient added successfully"
- Patient appears in the table
- Dialog closes

### Test 5.2: Search Patient

1. **In the search box, type:** `John`

**Expected Result:**
- Only matching patients are shown
- John Doe appears in the list

### Test 5.3: Edit Patient

1. **Select John Doe from the list**
2. **Click "Edit Patient"**
3. **Change Age to:** `46`
4. **Click "Save"**

**Expected Result:**
- Success message: "Patient updated successfully"
- Updated information shows in table

---

## Step 6: Test Clinical Note Generation

### Test 6.1: Select Patient for Notes

1. **Double-click on John Doe** in the patient list

**Expected Result:**
- Switches to "Clinical Notes" tab
- Shows: "Selected: John Doe (Age: 46)"

### Test 6.2: Generate SOAP Note (Text Input)

1. **In the transcription area, type or paste:**
```
Patient complains of headache for 3 days. Pain is described as tension-type,
bilateral, non-throbbing. No fever, no visual changes, no neck stiffness.

Physical examination shows blood pressure 130/85, pulse 72, temperature 98.6F.
Neurological examination normal. No signs of meningismus.

Assessment: Tension-type headache, likely related to work stress.

Plan: Advised adequate rest, hydration, stress management.
Prescribed ibuprofen 400mg as needed. Follow-up in 5 days if no improvement.
```

2. **Select "SOAP" as note type**
3. **Click "Generate Clinical Note"**

**Expected Result:**
- Progress bar animates
- After 10-30 seconds, a structured SOAP note appears
- ICD-10 suggestions appear (should include R51 - Headache)

**Generated Note Should Include:**
```
Subjective:
[Patient's symptoms...]

Objective:
[Vital signs and examination findings...]

Assessment:
[Diagnosis]
ICD-10 Code: R51 — Headache

Plan:
[Treatment plan...]
```

### Test 6.3: Save Note to Database

1. **Review the generated note**
2. **Click "Save to Database"**

**Expected Result:**
- Success message: "Note saved to database successfully!"
- Note is associated with John Doe

---

## Step 7: Test Audio Features (Optional)

⚠️ **Note:** Audio testing requires a working microphone

### Test 7.1: Record Audio

1. **Select a patient**
2. **Click "Start Recording"**
3. **Speak clearly for 10-15 seconds:**
   ```
   Patient reports fever and cough for two days.
   Temperature is 101 degrees Fahrenheit.
   Chest is clear. Throat is red.
   Likely viral upper respiratory infection.
   ```
4. **Click "Stop Recording"**

**Expected Result:**
- Timer shows recording duration
- "Processing..." appears
- Text is transcribed and appears in the text area
- May take 30-60 seconds for first transcription (Whisper model download)

### Test 7.2: Upload Audio File

1. **Click "Upload Audio"**
2. **Select a WAV or MP3 file**

**Expected Result:**
- "Transcribing..." appears
- Transcribed text appears in text area

---

## Step 8: Test Export Features

### Test 8.1: Export to PDF

1. **Generate a note (from Test 6.2)**
2. **Click "Export PDF"**
3. **Choose save location:** `test_note.pdf`
4. **Click Save**

**Expected Result:**
- Success message: "Note exported to [path]"
- PDF file created with:
  - Professional header
  - Patient information
  - Clinical note content
  - Doctor signature

### Test 8.2: Export to DOCX

1. **Click "Export DOCX"**
2. **Choose save location:** `test_note.docx`
3. **Click Save**

**Expected Result:**
- Success message: "Note exported to [path]"
- DOCX file created with formatted content

---

## Step 9: Test ICD-10 Lookup

### Test 9.1: Automatic Suggestions

When you generate a note with keywords like "diabetes", "hypertension", "headache", the ICD-10 panel should show relevant codes:

**Test Input:**
```
Patient has type 2 diabetes and hypertension.
```

**Expected ICD Suggestions:**
- E11.9 — Type 2 diabetes mellitus without complications
- I10 — Essential (primary) hypertension

---

## Step 10: Test Settings Tab

1. **Go to "Settings" tab**
2. **Click "Check Ollama Connection"**

**Expected Result:**
- Shows: "✓ Ollama: Connected"
- Shows: "Whisper Model: base"
- Shows: "Total Patients: [number]"

---

## Troubleshooting Guide

### Issue: "Ollama not connected" message

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not responding, start Ollama
ollama serve

# Verify Llama3 is installed
ollama list
ollama pull llama3  # if not found
```

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Audio recording doesn't work

**Solution:**
1. Check microphone permissions in system settings
2. Test microphone in another application
3. Try selecting a different input device
4. On Linux, you may need: `sudo apt-get install portaudio19-dev`

### Issue: Whisper transcription is very slow

**Solution:**
- First transcription downloads the model (1-2 minutes)
- Subsequent transcriptions are faster
- Use smaller model: Change `whisper_model` to `tiny` in `data/config.json`

### Issue: "Database locked" error

**Solution:**
```bash
# Close all instances of the application
# Delete the lock file if it exists
rm data/patients.db-journal
```

### Issue: PDF export fails

**Solution:**
```bash
# Reinstall reportlab
pip uninstall reportlab
pip install reportlab
```

---

## Quick Smoke Test Checklist

Use this for quick verification:

- [ ] Application starts without errors
- [ ] Can create doctor account
- [ ] Can login successfully
- [ ] Can add a patient
- [ ] Can search for patient
- [ ] Can generate a SOAP note (even if Ollama not connected, UI should work)
- [ ] Can save note to database
- [ ] Can export to PDF
- [ ] Can export to DOCX
- [ ] Can logout

---

## Performance Benchmarks

**Expected Performance:**
- Application startup: 2-5 seconds
- Login: < 1 second
- Add patient: < 1 second
- Generate note (with Ollama): 10-60 seconds (depends on CPU)
- Whisper transcription: 5-30 seconds per minute of audio
- PDF export: 1-3 seconds
- DOCX export: 1-2 seconds

---

## Testing Without Ollama

If you want to test the application without setting up Ollama:

1. All UI features will work
2. Patient management will work
3. Note generation will show "Ollama not connected" error
4. You can manually type notes in the output area
5. Export features will work with manually entered notes

---

## Advanced Testing

### Test Database Integrity

```bash
# Check database structure
sqlite3 data/patients.db ".schema"

# View doctors table
sqlite3 data/patients.db "SELECT * FROM doctors;"

# View patients table
sqlite3 data/patients.db "SELECT * FROM patients;"
```

### Test Encryption

```python
# Run Python interpreter
python

# Test encryption
from modules.encryption_manager import EncryptionManager
em = EncryptionManager()
encrypted = em.encrypt("Test data")
print(encrypted)
decrypted = em.decrypt(encrypted)
print(decrypted)  # Should print "Test data"
```

---

## Need Help?

If you encounter issues:

1. Check the error message in the terminal
2. Review this troubleshooting guide
3. Check README.md for additional information
4. Verify all prerequisites are met
5. Try the automated test: `python test_installation.py`

---

## Success Criteria

Your installation is successful if:

✅ Application launches without errors
✅ Can create and login with doctor account
✅ Can perform all CRUD operations on patients
✅ Can generate notes (with or without Ollama)
✅ Can export to PDF and DOCX
✅ Database persists data between sessions
✅ No crashes or freezes during normal use

---

**Ready to test? Start with Step 1!** 🚀
