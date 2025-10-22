"""
LLM Processing Module for AI Clinical Notes Assistant
Uses Ollama (Llama 3) for local AI note generation
"""
import requests
import json
from pathlib import Path

class LLMProcessor:
    def __init__(self, ollama_url="http://localhost:11434", model="llama3"):
        """
        Initialize LLM processor
        Args:
            ollama_url: URL of Ollama API
            model: Model name to use
        """
        self.ollama_url = ollama_url
        self.model = model
        self.api_endpoint = f"{ollama_url}/api/generate"

    def check_connection(self):
        """
        Check if Ollama is running
        Returns:
            True if connected, False otherwise
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def generate_note(self, transcription, note_type, template=None):
        """
        Generate clinical note using LLM
        Args:
            transcription: Transcribed patient consultation text
            note_type: Type of note (SOAP, Referral, Discharge)
            template: Optional prompt template
        Returns:
            Generated note text or None if error
        """
        if not self.check_connection():
            return None

        # Build prompt based on note type
        if template:
            prompt = template.replace("{transcription}", transcription)
        else:
            prompt = self._build_prompt(transcription, note_type)

        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"Error from Ollama: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print("Request to Ollama timed out")
            return None
        except Exception as e:
            print(f"Error generating note: {e}")
            return None

    def generate_note_stream(self, transcription, note_type, template=None, callback=None):
        """
        Generate clinical note with streaming (for real-time updates)
        Args:
            transcription: Transcribed patient consultation text
            note_type: Type of note (SOAP, Referral, Discharge)
            template: Optional prompt template
            callback: Function to call with each chunk of generated text
        Returns:
            Complete generated note text
        """
        if not self.check_connection():
            return None

        # Build prompt based on note type
        if template:
            prompt = template.replace("{transcription}", transcription)
        else:
            prompt = self._build_prompt(transcription, note_type)

        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True,
                timeout=120
            )

            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            text = chunk.get('response', '')
                            full_response += text
                            if callback:
                                callback(text)
                        except json.JSONDecodeError:
                            continue
                return full_response.strip()
            else:
                return None

        except Exception as e:
            print(f"Error in streaming generation: {e}")
            return None

    def _build_prompt(self, transcription, note_type):
        """
        Build prompt for note generation
        Args:
            transcription: Patient consultation text
            note_type: SOAP, Referral, or Discharge
        Returns:
            Formatted prompt
        """
        base_instruction = """You are an AI medical documentation assistant.
Convert the following patient consultation into a structured clinical note.
Include a likely ICD-10 code based on the described condition.
Do not make new diagnoses or give treatment advice - only document what is stated.
Be concise and professional."""

        if note_type.upper() == "SOAP":
            format_instruction = """
Format the note as follows:

Subjective:
[Patient's reported symptoms, complaints, and medical history]

Objective:
[Physical examination findings, vital signs, test results]

Assessment:
[Clinical impression and diagnosis]
ICD-10 Code: [Code] — [Description]

Plan:
[Treatment plan, medications, follow-up instructions]
"""

        elif note_type.upper() == "REFERRAL":
            format_instruction = """
Format the note as follows:

Patient Information:
[Name, age, relevant demographics]

Reason for Referral:
[Primary concern requiring specialist consultation]

Clinical History:
[Relevant medical history and current condition]

Assessment:
[Current diagnosis]
ICD-10 Code: [Code] — [Description]

Requested Action:
[Specific evaluation or treatment needed from specialist]
"""

        elif note_type.upper() == "DISCHARGE":
            format_instruction = """
Format the note as follows:

Patient Summary:
[Brief overview of hospital stay]

Admission Diagnosis:
[Reason for admission]

Hospital Course:
[Treatment provided and patient progress]

Discharge Diagnosis:
[Final diagnosis]
ICD-10 Code: [Code] — [Description]

Discharge Instructions:
[Medications, activity restrictions, follow-up care]

Follow-up:
[Appointments and monitoring needed]
"""
        else:
            format_instruction = "\n\nProvide a clear, structured clinical note."

        prompt = f"""{base_instruction}
{format_instruction}

Patient Consultation:
{transcription}

Generate the clinical note now:"""

        return prompt

    def suggest_icd_codes(self, text):
        """
        Use LLM to suggest ICD codes based on clinical text
        Args:
            text: Clinical text to analyze
        Returns:
            List of suggested ICD codes
        """
        if not self.check_connection():
            return []

        prompt = f"""Based on the following clinical text, suggest the most relevant ICD-10 codes.
Provide only the codes and their descriptions, one per line, in format: CODE — Description

Clinical text:
{text}

ICD-10 suggestions:"""

        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                suggestions_text = result.get('response', '').strip()
                # Parse the response to extract codes
                codes = []
                for line in suggestions_text.split('\n'):
                    if '—' in line or '-' in line:
                        codes.append(line.strip())
                return codes[:5]  # Return top 5 suggestions

        except Exception as e:
            print(f"Error suggesting ICD codes: {e}")

        return []
