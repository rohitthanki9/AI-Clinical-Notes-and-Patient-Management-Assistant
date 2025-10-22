"""
ICD-10 Code Lookup for AI Clinical Notes Assistant
Provides common ICD-10 diagnostic codes
"""
import json
from pathlib import Path

class ICDLookup:
    def __init__(self):
        """Initialize ICD-10 code dictionary"""
        self.icd_codes = {
            # Common symptoms
            "R51": "Headache",
            "R50.9": "Fever, unspecified",
            "R05": "Cough",
            "R06.02": "Shortness of breath",
            "R53.83": "Fatigue",
            "R11.0": "Nausea",
            "R11.2": "Nausea with vomiting",
            "R10.9": "Abdominal pain, unspecified",
            "R07.9": "Chest pain, unspecified",
            "R42": "Dizziness and giddiness",
            "R51.9": "Headache, unspecified",
            "R68.83": "Chills",

            # Cardiovascular
            "I10": "Essential (primary) hypertension",
            "I11.0": "Hypertensive heart disease with heart failure",
            "I25.10": "Atherosclerotic heart disease",
            "I48.91": "Atrial fibrillation",
            "I50.9": "Heart failure, unspecified",
            "I21.9": "Acute myocardial infarction",
            "I63.9": "Cerebral infarction, unspecified",

            # Respiratory
            "J06.9": "Upper respiratory infection",
            "J02.9": "Acute pharyngitis",
            "J20.9": "Acute bronchitis",
            "J18.9": "Pneumonia, unspecified",
            "J45.909": "Asthma, unspecified",
            "J44.0": "COPD with acute lower respiratory infection",
            "J44.1": "COPD with acute exacerbation",

            # Endocrine/Metabolic
            "E11.9": "Type 2 diabetes mellitus without complications",
            "E11.65": "Type 2 diabetes with hyperglycemia",
            "E78.5": "Hyperlipidemia",
            "E66.9": "Obesity, unspecified",
            "E03.9": "Hypothyroidism, unspecified",
            "E05.90": "Hyperthyroidism, unspecified",

            # Gastrointestinal
            "K21.9": "Gastro-esophageal reflux disease",
            "K29.70": "Gastritis, unspecified",
            "K58.9": "Irritable bowel syndrome",
            "K59.00": "Constipation, unspecified",
            "K52.9": "Gastroenteritis and colitis",

            # Musculoskeletal
            "M25.50": "Pain in joint, unspecified",
            "M79.3": "Panniculitis, unspecified",
            "M54.5": "Low back pain",
            "M79.1": "Myalgia",
            "M25.561": "Pain in right knee",
            "M25.562": "Pain in left knee",

            # Mental Health
            "F41.1": "Generalized anxiety disorder",
            "F32.9": "Major depressive disorder, single episode",
            "F33.1": "Major depressive disorder, recurrent",
            "F41.9": "Anxiety disorder, unspecified",
            "F43.10": "Post-traumatic stress disorder",

            # Neurological
            "G43.909": "Migraine, unspecified",
            "G89.29": "Chronic pain",
            "G47.00": "Insomnia, unspecified",

            # Infectious
            "B34.9": "Viral infection, unspecified",
            "A09": "Infectious gastroenteritis",
            "J03.90": "Acute tonsillitis, unspecified",

            # Dermatological
            "L30.9": "Dermatitis, unspecified",
            "L50.9": "Urticaria, unspecified",
            "L70.0": "Acne vulgaris",

            # Urinary
            "N39.0": "Urinary tract infection",
            "N18.3": "Chronic kidney disease, stage 3",
            "N40.0": "Benign prostatic hyperplasia",

            # General
            "Z00.00": "General adult medical examination",
            "Z23": "Immunization",
            "Z79.4": "Long-term use of insulin",
            "Z79.899": "Long-term use of other medications"
        }

        # Reverse lookup for searching
        self.code_to_description = self.icd_codes
        self.description_to_code = {v.lower(): k for k, v in self.icd_codes.items()}

    def search_by_code(self, code):
        """
        Search for description by ICD code
        Args:
            code: ICD-10 code (e.g., 'R51')
        Returns:
            Description or None
        """
        return self.icd_codes.get(code.upper())

    def search_by_description(self, description):
        """
        Search for ICD code by description
        Args:
            description: Condition description
        Returns:
            ICD code or None
        """
        desc_lower = description.lower()

        # Exact match
        if desc_lower in self.description_to_code:
            return self.description_to_code[desc_lower]

        # Partial match
        for desc, code in self.description_to_code.items():
            if desc in desc_lower or desc_lower in desc:
                return code

        return None

    def search(self, query):
        """
        Search for ICD codes by query string
        Args:
            query: Search term
        Returns:
            List of matching (code, description) tuples
        """
        query_lower = query.lower()
        results = []

        for code, description in self.icd_codes.items():
            if (query_lower in code.lower() or
                query_lower in description.lower()):
                results.append((code, description))

        return results

    def get_all_codes(self):
        """Get all ICD codes"""
        return sorted(self.icd_codes.items())

    def suggest_codes(self, text):
        """
        Suggest relevant ICD codes based on text
        Args:
            text: Clinical text to analyze
        Returns:
            List of suggested (code, description) tuples
        """
        text_lower = text.lower()
        suggestions = []

        # Keywords to ICD code mapping
        keyword_mapping = {
            'headache': ['R51', 'G43.909'],
            'fever': ['R50.9'],
            'cough': ['R05', 'J20.9'],
            'diabetes': ['E11.9', 'E11.65'],
            'hypertension': ['I10'],
            'pain': ['M79.1', 'G89.29'],
            'chest pain': ['R07.9'],
            'back pain': ['M54.5'],
            'anxiety': ['F41.1', 'F41.9'],
            'depression': ['F32.9', 'F33.1'],
            'asthma': ['J45.909'],
            'pneumonia': ['J18.9'],
            'nausea': ['R11.0'],
            'vomiting': ['R11.2'],
            'dizziness': ['R42'],
            'fatigue': ['R53.83'],
            'obesity': ['E66.9'],
            'infection': ['B34.9'],
            'uti': ['N39.0'],
            'gastritis': ['K29.70'],
        }

        for keyword, codes in keyword_mapping.items():
            if keyword in text_lower:
                for code in codes:
                    if code in self.icd_codes:
                        suggestions.append((code, self.icd_codes[code]))

        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for item in suggestions:
            if item[0] not in seen:
                seen.add(item[0])
                unique_suggestions.append(item)

        return unique_suggestions
