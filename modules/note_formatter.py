"""
Note Formatter for AI Clinical Notes Assistant
Formats and validates clinical notes
"""
from datetime import datetime
import re

class NoteFormatter:
    def __init__(self):
        """Initialize note formatter"""
        pass

    def format_soap_note(self, content, patient_info=None, doctor_info=None):
        """
        Format a SOAP note with headers and metadata
        Args:
            content: Raw note content
            patient_info: Dictionary with patient details
            doctor_info: Dictionary with doctor details
        Returns:
            Formatted note string
        """
        header = self._create_header("SOAP Note", patient_info, doctor_info)
        formatted = f"{header}\n\n{content}"
        return formatted

    def format_referral_note(self, content, patient_info=None, doctor_info=None):
        """
        Format a referral note with headers and metadata
        Args:
            content: Raw note content
            patient_info: Dictionary with patient details
            doctor_info: Dictionary with doctor details
        Returns:
            Formatted note string
        """
        header = self._create_header("Referral Note", patient_info, doctor_info)
        formatted = f"{header}\n\n{content}"
        return formatted

    def format_discharge_note(self, content, patient_info=None, doctor_info=None):
        """
        Format a discharge note with headers and metadata
        Args:
            content: Raw note content
            patient_info: Dictionary with patient details
            doctor_info: Dictionary with doctor details
        Returns:
            Formatted note string
        """
        header = self._create_header("Discharge Summary", patient_info, doctor_info)
        formatted = f"{header}\n\n{content}"
        return formatted

    def _create_header(self, note_type, patient_info=None, doctor_info=None):
        """
        Create note header with metadata
        Args:
            note_type: Type of note
            patient_info: Patient details
            doctor_info: Doctor details
        Returns:
            Formatted header string
        """
        header_lines = []
        header_lines.append("=" * 70)
        header_lines.append(f"{note_type}".center(70))
        header_lines.append("=" * 70)
        header_lines.append("")

        # Date and time
        now = datetime.now()
        header_lines.append(f"Date: {now.strftime('%Y-%m-%d')}")
        header_lines.append(f"Time: {now.strftime('%H:%M:%S')}")
        header_lines.append("")

        # Patient information
        if patient_info:
            header_lines.append("PATIENT INFORMATION:")
            header_lines.append(f"Name: {patient_info.get('name', 'N/A')}")
            if patient_info.get('age'):
                header_lines.append(f"Age: {patient_info.get('age')} years")
            if patient_info.get('gender'):
                header_lines.append(f"Gender: {patient_info.get('gender')}")
            if patient_info.get('contact'):
                header_lines.append(f"Contact: {patient_info.get('contact')}")
            header_lines.append("")

        # Doctor information
        if doctor_info:
            header_lines.append("PROVIDER INFORMATION:")
            header_lines.append(f"Doctor: {doctor_info.get('name', 'N/A')}")
            if doctor_info.get('email'):
                header_lines.append(f"Email: {doctor_info.get('email')}")
            header_lines.append("")

        header_lines.append("-" * 70)
        header_lines.append("")

        return "\n".join(header_lines)

    def extract_icd_codes(self, note_content):
        """
        Extract ICD-10 codes from note content
        Args:
            note_content: Clinical note text
        Returns:
            List of ICD codes found
        """
        # Pattern to match ICD-10 codes
        pattern = r'\b[A-Z]\d{2}(?:\.\d{1,4})?\b'
        matches = re.findall(pattern, note_content)
        return list(set(matches))  # Remove duplicates

    def validate_note(self, note_content, note_type):
        """
        Validate that a note contains required sections
        Args:
            note_content: Note content to validate
            note_type: Type of note (SOAP, Referral, Discharge)
        Returns:
            Tuple of (is_valid, missing_sections)
        """
        missing_sections = []

        if note_type.upper() == "SOAP":
            required_sections = ["Subjective", "Objective", "Assessment", "Plan"]
        elif note_type.upper() == "REFERRAL":
            required_sections = ["Reason for Referral", "Clinical History", "Assessment"]
        elif note_type.upper() == "DISCHARGE":
            required_sections = ["Admission Diagnosis", "Hospital Course", "Discharge Diagnosis"]
        else:
            return True, []

        for section in required_sections:
            if section.lower() not in note_content.lower():
                missing_sections.append(section)

        is_valid = len(missing_sections) == 0
        return is_valid, missing_sections

    def clean_note(self, note_content):
        """
        Clean and normalize note content
        Args:
            note_content: Raw note content
        Returns:
            Cleaned note content
        """
        # Remove excessive whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', note_content)
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        return cleaned

    def add_signature(self, note_content, doctor_info):
        """
        Add doctor's signature to note
        Args:
            note_content: Note content
            doctor_info: Doctor information
        Returns:
            Note with signature
        """
        signature_lines = [
            "",
            "",
            "-" * 70,
            "Electronically signed by:",
            f"Dr. {doctor_info.get('name', 'Unknown')}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 70
        ]

        return note_content + "\n" + "\n".join(signature_lines)

    def format_for_export(self, note_content, note_type, patient_info, doctor_info):
        """
        Format note for export (PDF/DOCX)
        Args:
            note_content: Raw note content
            note_type: Type of note
            patient_info: Patient information
            doctor_info: Doctor information
        Returns:
            Fully formatted note ready for export
        """
        # Format based on type
        if note_type.upper() == "SOAP":
            formatted = self.format_soap_note(note_content, patient_info, doctor_info)
        elif note_type.upper() == "REFERRAL":
            formatted = self.format_referral_note(note_content, patient_info, doctor_info)
        elif note_type.upper() == "DISCHARGE":
            formatted = self.format_discharge_note(note_content, patient_info, doctor_info)
        else:
            formatted = note_content

        # Clean the note
        formatted = self.clean_note(formatted)

        # Add signature
        formatted = self.add_signature(formatted, doctor_info)

        return formatted
