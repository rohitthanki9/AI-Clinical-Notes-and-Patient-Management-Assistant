#!/usr/bin/env python3
"""
AI Clinical Notes and Patient Management Assistant
Main application entry point

A standalone, offline desktop application for doctors and clinicians to:
- Record/upload voice and transcribe to text (Whisper)
- Generate structured clinical notes (SOAP/Referral/Discharge) using local LLM (Llama 3 via Ollama)
- Manage patients with ICD-10 diagnostic codes
- Encrypt and store notes securely (AES-256)
- Export notes as PDF or DOCX

Author: AI Clinical Notes Team
Version: 1.0
"""

import sys
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.config_manager import ConfigManager
from modules.patient_db import PatientDatabase
from modules.encryption_manager import EncryptionManager
from modules.icd_lookup import ICDLookup
from modules.speech_to_text import SpeechToText
from modules.llm_processing_ollama import LLMProcessor
from modules.note_formatter import NoteFormatter
from modules.export_manager import ExportManager
from modules.gui_login import LoginWindow
from modules.gui_dashboard import DashboardWindow


class ClinicalNotesApp:
    """Main application class"""

    def __init__(self):
        """Initialize the application"""
        print("Initializing AI Clinical Notes and Patient Management Assistant...")

        # Initialize configuration
        self.config = ConfigManager()
        print(" Configuration loaded")

        # Initialize database
        db_path = self.config.get('db_path')
        self.db = PatientDatabase(db_path)
        print(" Database initialized")

        # Initialize encryption
        key_path = self.config.get('encryption_key_path')
        self.encryption = EncryptionManager(key_path)
        print(" Encryption manager initialized")

        # Initialize ICD lookup
        self.icd_lookup = ICDLookup()
        print(" ICD-10 lookup loaded")

        # Initialize speech-to-text
        whisper_model = self.config.get('whisper_model', 'base')
        self.stt = SpeechToText(whisper_model)
        print(f" Speech-to-text ready (Whisper model: {whisper_model})")

        # Initialize LLM processor
        ollama_url = self.config.get('ollama_url')
        ollama_model = self.config.get('ollama_model')
        self.llm = LLMProcessor(ollama_url, ollama_model)
        print(f" LLM processor ready (Model: {ollama_model})")

        # Check Ollama connection
        if self.llm.check_connection():
            print(" Ollama connection: OK")
        else:
            print(" Warning: Ollama not connected. AI features will not work.")
            print(f"   Please start Ollama and ensure {ollama_model} is installed.")

        # Initialize note formatter
        self.note_formatter = NoteFormatter()
        print(" Note formatter ready")

        # Initialize export manager
        clinic_name = self.config.get('clinic_name')
        self.export_manager = ExportManager(clinic_name)
        print(" Export manager ready")

        print("\nApplication initialized successfully!\n")

    def run(self):
        """Run the application"""
        print("Starting application...")

        # Show login window
        def on_login_success(doctor_info):
            """Callback when login is successful"""
            print(f"\nDoctor logged in: {doctor_info['name']}")

            # Launch dashboard
            dashboard = DashboardWindow(
                doctor_info=doctor_info,
                db_manager=self.db,
                config_manager=self.config,
                stt_module=self.stt,
                llm_module=self.llm,
                icd_lookup=self.icd_lookup,
                note_formatter=self.note_formatter,
                export_manager=self.export_manager
            )

            dashboard.run()

        # Show login window
        login = LoginWindow(self.db, on_login_success)
        login.run()

        print("\nApplication closed. Goodbye!")

    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'db'):
            self.db.close()


def main():
    """Main entry point"""
    print("=" * 70)
    print("AI Clinical Notes and Patient Management Assistant".center(70))
    print("Offline Medical Documentation System".center(70))
    print("=" * 70)
    print()

    try:
        app = ClinicalNotesApp()
        app.run()
        app.cleanup()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
