"""
Patient Database Manager for AI Clinical Notes Assistant
Handles all database operations for doctors and patients
"""
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

class PatientDatabase:
    def __init__(self, db_path=None):
        """
        Initialize database connection
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "patients.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Doctors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                date_created TEXT NOT NULL
            )
        ''')

        # Patients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                contact TEXT,
                diagnosis TEXT,
                icd_code TEXT,
                notes TEXT,
                date_created TEXT NOT NULL,
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')

        # Clinical notes table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clinical_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                note_type TEXT NOT NULL,
                content TEXT NOT NULL,
                icd_codes TEXT,
                date_created TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')

        self.conn.commit()

    # ==================== Doctor Methods ====================

    def create_doctor(self, name, email, password):
        """
        Create a new doctor account
        Args:
            name: Doctor's name
            email: Doctor's email
            password: Plain text password (will be hashed)
        Returns:
            Doctor ID if successful, None otherwise
        """
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                INSERT INTO doctors (name, email, password_hash, date_created)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password_hash, date_created))

            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Email already exists
        except Exception as e:
            print(f"Error creating doctor: {e}")
            return None

    def authenticate_doctor(self, email, password):
        """
        Authenticate a doctor
        Args:
            email: Doctor's email
            password: Plain text password
        Returns:
            Doctor record if successful, None otherwise
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute('''
            SELECT * FROM doctors WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))

        result = self.cursor.fetchone()
        return dict(result) if result else None

    def get_doctor_by_id(self, doctor_id):
        """Get doctor information by ID"""
        self.cursor.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,))
        result = self.cursor.fetchone()
        return dict(result) if result else None

    # ==================== Patient Methods ====================

    def create_patient(self, doctor_id, name, age=None, gender=None, contact=None,
                       diagnosis=None, icd_code=None, notes=None):
        """
        Create a new patient record
        Args:
            doctor_id: ID of the doctor creating the patient
            name: Patient's name
            age: Patient's age
            gender: Patient's gender
            contact: Contact information
            diagnosis: Initial diagnosis
            icd_code: ICD-10 code
            notes: Additional notes
        Returns:
            Patient ID if successful, None otherwise
        """
        try:
            date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                INSERT INTO patients (doctor_id, name, age, gender, contact,
                                     diagnosis, icd_code, notes, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (doctor_id, name, age, gender, contact, diagnosis, icd_code, notes, date_created))

            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating patient: {e}")
            return None

    def get_patient(self, patient_id):
        """Get patient by ID"""
        self.cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        result = self.cursor.fetchone()
        return dict(result) if result else None

    def get_all_patients(self, doctor_id):
        """Get all patients for a specific doctor"""
        self.cursor.execute('''
            SELECT * FROM patients WHERE doctor_id = ? ORDER BY date_created DESC
        ''', (doctor_id,))
        return [dict(row) for row in self.cursor.fetchall()]

    def update_patient(self, patient_id, **kwargs):
        """
        Update patient information
        Args:
            patient_id: ID of patient to update
            **kwargs: Fields to update (name, age, gender, contact, diagnosis, icd_code, notes)
        """
        try:
            allowed_fields = ['name', 'age', 'gender', 'contact', 'diagnosis', 'icd_code', 'notes']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

            if not updates:
                return False

            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [patient_id]

            self.cursor.execute(f'''
                UPDATE patients SET {set_clause} WHERE id = ?
            ''', values)

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False

    def delete_patient(self, patient_id):
        """Delete a patient record"""
        try:
            # Also delete associated clinical notes
            self.cursor.execute('DELETE FROM clinical_notes WHERE patient_id = ?', (patient_id,))
            self.cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False

    def search_patients(self, doctor_id, query):
        """
        Search patients by name, diagnosis, or ICD code
        Args:
            doctor_id: ID of the doctor
            query: Search term
        Returns:
            List of matching patients
        """
        search_term = f"%{query}%"
        self.cursor.execute('''
            SELECT * FROM patients
            WHERE doctor_id = ? AND (
                name LIKE ? OR
                diagnosis LIKE ? OR
                icd_code LIKE ?
            )
            ORDER BY date_created DESC
        ''', (doctor_id, search_term, search_term, search_term))

        return [dict(row) for row in self.cursor.fetchall()]

    # ==================== Clinical Notes Methods ====================

    def create_clinical_note(self, patient_id, doctor_id, note_type, content, icd_codes=None):
        """
        Create a clinical note
        Args:
            patient_id: Patient ID
            doctor_id: Doctor ID
            note_type: Type of note (SOAP, Referral, Discharge)
            content: Note content
            icd_codes: Associated ICD codes
        Returns:
            Note ID if successful, None otherwise
        """
        try:
            date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                INSERT INTO clinical_notes (patient_id, doctor_id, note_type, content,
                                           icd_codes, date_created)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (patient_id, doctor_id, note_type, content, icd_codes, date_created))

            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating clinical note: {e}")
            return None

    def get_patient_notes(self, patient_id):
        """Get all clinical notes for a patient"""
        self.cursor.execute('''
            SELECT * FROM clinical_notes WHERE patient_id = ? ORDER BY date_created DESC
        ''', (patient_id,))
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        """Close database connection"""
        self.conn.close()
