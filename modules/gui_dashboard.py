"""
Dashboard GUI for AI Clinical Notes Assistant
Main application interface for managing patients and notes
"""
import tkinter as tk
from tkinter import messagebox, filedialog, ttk as tkttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
import threading
from pathlib import Path
from datetime import datetime

class DashboardWindow:
    def __init__(self, doctor_info, db_manager, config_manager,
                 stt_module, llm_module, icd_lookup, note_formatter, export_manager):
        """
        Initialize dashboard window
        Args:
            doctor_info: Dictionary with logged-in doctor information
            db_manager: PatientDatabase instance
            config_manager: ConfigManager instance
            stt_module: SpeechToText instance
            llm_module: LLMProcessor instance
            icd_lookup: ICDLookup instance
            note_formatter: NoteFormatter instance
            export_manager: ExportManager instance
        """
        self.doctor = doctor_info
        self.db = db_manager
        self.config = config_manager
        self.stt = stt_module
        self.llm = llm_module
        self.icd = icd_lookup
        self.formatter = note_formatter
        self.exporter = export_manager

        self.current_patient = None
        self.is_recording = False
        self.generated_note = ""

        # Create main window
        self.root = ttk.Window(themename="flatly")
        self.root.title("AI Clinical Notes - Dashboard")
        self.root.geometry("1400x900")

        # Create UI
        self.create_dashboard_ui()

        # Load initial data
        self.refresh_patients()

    def create_dashboard_ui(self):
        """Create main dashboard interface"""
        # Header
        self.create_header()

        # Main content area with notebook
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Create tabs
        self.create_patients_tab()
        self.create_notes_tab()
        self.create_settings_tab()

    def create_header(self):
        """Create header with doctor info and logout"""
        header = ttk.Frame(self.root, bootstyle="primary")
        header.pack(fill=X, padx=10, pady=(10, 0))

        # Left side - Title
        title_label = ttk.Label(
            header,
            text=" AI Clinical Notes & Patient Management",
            font=("Segoe UI", 16, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(side=LEFT, padx=10, pady=10)

        # Right side - Doctor info and logout
        info_frame = ttk.Frame(header, bootstyle="primary")
        info_frame.pack(side=RIGHT, padx=10, pady=10)

        doctor_label = ttk.Label(
            info_frame,
            text=f"Dr. {self.doctor['name']}",
            font=("Segoe UI", 11),
            bootstyle="inverse-primary"
        )
        doctor_label.pack(side=LEFT, padx=10)

        logout_btn = ttk.Button(
            info_frame,
            text="Logout",
            command=self.handle_logout,
            bootstyle="danger-outline",
            width=10
        )
        logout_btn.pack(side=LEFT)

    # ==================== PATIENTS TAB ====================

    def create_patients_tab(self):
        """Create patients management tab"""
        patients_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(patients_frame, text=" Patients ")

        # Top controls
        controls_frame = ttk.Frame(patients_frame)
        controls_frame.pack(fill=X, pady=(0, 10))

        # Search bar
        search_frame = ttk.Frame(controls_frame)
        search_frame.pack(side=LEFT, fill=X, expand=YES)

        ttk.Label(search_frame, text="Search:", font=("Segoe UI", 11)).pack(side=LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_patients())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=LEFT, padx=5)

        # Buttons
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.pack(side=RIGHT)

        ttk.Button(
            btn_frame,
            text=" Add Patient",
            command=self.add_patient_dialog,
            bootstyle="success"
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text=" Edit Patient",
            command=self.edit_patient_dialog,
            bootstyle="info"
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text=" Delete Patient",
            command=self.delete_patient,
            bootstyle="danger"
        ).pack(side=LEFT, padx=5)

        # Patients table
        table_frame = ttk.Frame(patients_frame)
        table_frame.pack(fill=BOTH, expand=YES)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient=VERTICAL)
        y_scroll.pack(side=RIGHT, fill=Y)

        x_scroll = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        x_scroll.pack(side=BOTTOM, fill=X)

        # Treeview
        columns = ("ID", "Name", "Age", "Gender", "Contact", "Diagnosis", "ICD Code", "Date")
        self.patients_tree = tkttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        # Configure columns
        self.patients_tree.heading("ID", text="ID")
        self.patients_tree.heading("Name", text="Name")
        self.patients_tree.heading("Age", text="Age")
        self.patients_tree.heading("Gender", text="Gender")
        self.patients_tree.heading("Contact", text="Contact")
        self.patients_tree.heading("Diagnosis", text="Diagnosis")
        self.patients_tree.heading("ICD Code", text="ICD Code")
        self.patients_tree.heading("Date", text="Date Added")

        self.patients_tree.column("ID", width=50)
        self.patients_tree.column("Name", width=150)
        self.patients_tree.column("Age", width=60)
        self.patients_tree.column("Gender", width=80)
        self.patients_tree.column("Contact", width=120)
        self.patients_tree.column("Diagnosis", width=200)
        self.patients_tree.column("ICD Code", width=100)
        self.patients_tree.column("Date", width=120)

        self.patients_tree.pack(fill=BOTH, expand=YES)

        y_scroll.config(command=self.patients_tree.yview)
        x_scroll.config(command=self.patients_tree.xview)

        # Bind double-click to select patient
        self.patients_tree.bind('<Double-1>', lambda e: self.select_patient_for_notes())

    # ==================== NOTES TAB ====================

    def create_notes_tab(self):
        """Create clinical notes generation tab"""
        notes_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(notes_frame, text=" Clinical Notes ")

        # Left panel - Input and controls
        left_panel = ttk.Frame(notes_frame)
        left_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Patient selection
        patient_frame = ttk.Labelframe(left_panel, text="Patient Selection", padding=10)
        patient_frame.pack(fill=X, pady=(0, 10))

        self.selected_patient_label = ttk.Label(
            patient_frame,
            text="No patient selected. Double-click a patient in the Patients tab.",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.selected_patient_label.pack()

        # Transcription input
        input_frame = ttk.Labelframe(left_panel, text="Patient Consultation / Transcription", padding=10)
        input_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Audio controls
        audio_controls = ttk.Frame(input_frame)
        audio_controls.pack(fill=X, pady=(0, 10))

        self.record_btn = ttk.Button(
            audio_controls,
            text=" Start Recording",
            command=self.toggle_recording,
            bootstyle="danger-outline"
        )
        self.record_btn.pack(side=LEFT, padx=5)

        ttk.Button(
            audio_controls,
            text=" Upload Audio",
            command=self.upload_audio,
            bootstyle="info-outline"
        ).pack(side=LEFT, padx=5)

        self.recording_label = ttk.Label(
            audio_controls,
            text="",
            font=("Segoe UI", 9),
            bootstyle="danger"
        )
        self.recording_label.pack(side=LEFT, padx=10)

        # Text input
        self.transcription_text = ScrolledText(
            input_frame,
            height=15,
            autohide=True
        )
        self.transcription_text.pack(fill=BOTH, expand=YES)

        # Note type selection
        type_frame = ttk.Frame(left_panel)
        type_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(type_frame, text="Note Type:", font=("Segoe UI", 11)).pack(side=LEFT, padx=(0, 10))
        self.note_type_var = tk.StringVar(value="SOAP")
        for note_type in ["SOAP", "Referral", "Discharge"]:
            ttk.Radiobutton(
                type_frame,
                text=note_type,
                variable=self.note_type_var,
                value=note_type,
                bootstyle="primary"
            ).pack(side=LEFT, padx=5)

        # Generate button
        self.generate_btn = ttk.Button(
            left_panel,
            text=" Generate Clinical Note",
            command=self.generate_note,
            bootstyle="success",
            width=30
        )
        self.generate_btn.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(
            left_panel,
            mode='indeterminate',
            bootstyle="success-striped"
        )
        self.progress.pack(fill=X, pady=(0, 10))

        # Right panel - Generated note
        right_panel = ttk.Frame(notes_frame)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Generated note display
        note_frame = ttk.Labelframe(right_panel, text="Generated Clinical Note", padding=10)
        note_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        self.note_display = ScrolledText(
            note_frame,
            height=25,
            autohide=True
        )
        self.note_display.pack(fill=BOTH, expand=YES)

        # ICD code suggestions
        icd_frame = ttk.Labelframe(right_panel, text="ICD-10 Code Suggestions", padding=10)
        icd_frame.pack(fill=X, pady=(0, 10))

        self.icd_listbox = tk.Listbox(icd_frame, height=5, font=("Segoe UI", 10))
        self.icd_listbox.pack(fill=X)

        # Export buttons
        export_frame = ttk.Frame(right_panel)
        export_frame.pack(fill=X)

        ttk.Button(
            export_frame,
            text=" Save to Database",
            command=self.save_note,
            bootstyle="primary"
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        ttk.Button(
            export_frame,
            text=" Export PDF",
            command=self.export_pdf,
            bootstyle="info"
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

        ttk.Button(
            export_frame,
            text=" Export DOCX",
            command=self.export_docx,
            bootstyle="info"
        ).pack(side=LEFT, padx=5, fill=X, expand=YES)

    # ==================== SETTINGS TAB ====================

    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(settings_frame, text=" Settings ")

        # System status
        status_frame = ttk.Labelframe(settings_frame, text="System Status", padding=15)
        status_frame.pack(fill=X, pady=(0, 20))

        # Ollama status
        self.ollama_status = ttk.Label(
            status_frame,
            text="Checking Ollama status...",
            font=("Segoe UI", 11)
        )
        self.ollama_status.pack(anchor=W, pady=5)

        ttk.Button(
            status_frame,
            text="Check Ollama Connection",
            command=self.check_ollama_status,
            bootstyle="info-outline"
        ).pack(anchor=W, pady=5)

        # Whisper status
        whisper_status = ttk.Label(
            status_frame,
            text=f"Whisper Model: {self.config.get('whisper_model', 'base')}",
            font=("Segoe UI", 11)
        )
        whisper_status.pack(anchor=W, pady=5)

        # Database info
        patients_count = len(self.db.get_all_patients(self.doctor['id']))
        db_status = ttk.Label(
            status_frame,
            text=f"Total Patients: {patients_count}",
            font=("Segoe UI", 11)
        )
        db_status.pack(anchor=W, pady=5)

        # Check initial Ollama status
        self.check_ollama_status()

    # ==================== EVENT HANDLERS ====================

    def refresh_patients(self):
        """Refresh patients list"""
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        # Load patients
        patients = self.db.get_all_patients(self.doctor['id'])

        for patient in patients:
            self.patients_tree.insert('', END, values=(
                patient['id'],
                patient['name'],
                patient.get('age', 'N/A'),
                patient.get('gender', 'N/A'),
                patient.get('contact', 'N/A'),
                patient.get('diagnosis', 'N/A'),
                patient.get('icd_code', 'N/A'),
                patient['date_created'].split()[0]  # Date only
            ))

    def filter_patients(self):
        """Filter patients based on search"""
        query = self.search_var.get().strip()

        # Clear tree
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        if query:
            patients = self.db.search_patients(self.doctor['id'], query)
        else:
            patients = self.db.get_all_patients(self.doctor['id'])

        for patient in patients:
            self.patients_tree.insert('', END, values=(
                patient['id'],
                patient['name'],
                patient.get('age', 'N/A'),
                patient.get('gender', 'N/A'),
                patient.get('contact', 'N/A'),
                patient.get('diagnosis', 'N/A'),
                patient.get('icd_code', 'N/A'),
                patient['date_created'].split()[0]
            ))

    def add_patient_dialog(self):
        """Show add patient dialog"""
        dialog = PatientDialog(self.root, self.db, self.doctor['id'], callback=self.refresh_patients)

    def edit_patient_dialog(self):
        """Show edit patient dialog"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to edit")
            return

        patient_id = self.patients_tree.item(selected[0])['values'][0]
        patient = self.db.get_patient(patient_id)

        dialog = PatientDialog(
            self.root,
            self.db,
            self.doctor['id'],
            patient=patient,
            callback=self.refresh_patients
        )

    def delete_patient(self):
        """Delete selected patient"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to delete")
            return

        patient_id = self.patients_tree.item(selected[0])['values'][0]
        patient_name = self.patients_tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Confirm Delete", f"Delete patient {patient_name}?\nThis cannot be undone."):
            if self.db.delete_patient(patient_id):
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.refresh_patients()
            else:
                messagebox.showerror("Error", "Failed to delete patient")

    def select_patient_for_notes(self):
        """Select patient for creating notes"""
        selected = self.patients_tree.selection()
        if not selected:
            return

        patient_id = self.patients_tree.item(selected[0])['values'][0]
        self.current_patient = self.db.get_patient(patient_id)

        self.selected_patient_label.config(
            text=f"Selected: {self.current_patient['name']} (Age: {self.current_patient.get('age', 'N/A')})",
            bootstyle="success"
        )

        # Switch to notes tab
        self.notebook.select(1)

    def toggle_recording(self):
        """Toggle audio recording"""
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.record_btn.config(text=" Stop Recording", bootstyle="danger")
            self.recording_label.config(text=" Recording...")

            def update_timer(duration):
                mins = int(duration // 60)
                secs = int(duration % 60)
                self.recording_label.config(text=f" Recording... {mins:02d}:{secs:02d}")

            self.stt.start_recording(callback=update_timer)
        else:
            # Stop recording
            self.is_recording = False
            self.record_btn.config(text=" Start Recording", bootstyle="danger-outline")
            self.recording_label.config(text=" Processing...")

            def process_recording():
                audio_path = self.stt.stop_recording()
                if audio_path:
                    text = self.stt.transcribe_file(audio_path)
                    if text:
                        self.transcription_text.text.insert(END, text + "\n")
                        self.recording_label.config(text=" Transcription complete")
                    else:
                        self.recording_label.config(text=" Transcription failed")
                else:
                    self.recording_label.config(text=" Recording failed")

            threading.Thread(target=process_recording, daemon=True).start()

    def upload_audio(self):
        """Upload and transcribe audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.m4a"), ("All Files", "*.*")]
        )

        if file_path:
            self.recording_label.config(text=" Transcribing...")

            def transcribe():
                text = self.stt.transcribe_file(file_path)
                if text:
                    self.transcription_text.text.insert(END, text + "\n")
                    self.recording_label.config(text=" Transcription complete")
                else:
                    self.recording_label.config(text=" Transcription failed")
                    messagebox.showerror("Error", "Failed to transcribe audio file")

            threading.Thread(target=transcribe, daemon=True).start()

    def generate_note(self):
        """Generate clinical note using LLM"""
        transcription = self.transcription_text.text.get("1.0", END).strip()

        if not transcription:
            messagebox.showwarning("No Input", "Please enter or transcribe patient consultation text")
            return

        note_type = self.note_type_var.get()

        # Disable button and start progress
        self.generate_btn.config(state=DISABLED)
        self.progress.start()

        def generate():
            # Load template if available
            template = self.config.get_prompt_template(note_type.lower())

            # Generate note
            note = self.llm.generate_note(transcription, note_type, template)

            if note:
                self.generated_note = note
                self.note_display.text.delete("1.0", END)
                self.note_display.text.insert("1.0", note)

                # Extract and suggest ICD codes
                self.suggest_icd_codes(transcription + "\n" + note)

                messagebox.showinfo("Success", "Clinical note generated successfully!")
            else:
                messagebox.showerror("Error", "Failed to generate note. Ensure Ollama is running.")

            # Re-enable button and stop progress
            self.generate_btn.config(state=NORMAL)
            self.progress.stop()

        threading.Thread(target=generate, daemon=True).start()

    def suggest_icd_codes(self, text):
        """Suggest ICD codes based on text"""
        self.icd_listbox.delete(0, END)

        suggestions = self.icd.suggest_codes(text)

        if suggestions:
            for code, description in suggestions:
                self.icd_listbox.insert(END, f"{code} — {description}")
        else:
            self.icd_listbox.insert(END, "No ICD code suggestions")

    def save_note(self):
        """Save note to database"""
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please select a patient first")
            return

        note_content = self.note_display.text.get("1.0", END).strip()
        if not note_content:
            messagebox.showwarning("No Note", "Please generate a note first")
            return

        note_type = self.note_type_var.get()

        # Get selected ICD codes
        icd_codes = []
        for i in self.icd_listbox.curselection():
            icd_codes.append(self.icd_listbox.get(i).split(' — ')[0])

        icd_codes_str = ', '.join(icd_codes) if icd_codes else None

        # Save to database
        note_id = self.db.create_clinical_note(
            self.current_patient['id'],
            self.doctor['id'],
            note_type,
            note_content,
            icd_codes_str
        )

        if note_id:
            # Also update patient with diagnosis and ICD code
            if icd_codes:
                self.db.update_patient(
                    self.current_patient['id'],
                    icd_code=icd_codes[0]
                )

            messagebox.showinfo("Success", "Note saved to database successfully!")
            self.refresh_patients()
        else:
            messagebox.showerror("Error", "Failed to save note")

    def export_pdf(self):
        """Export note as PDF"""
        note_content = self.note_display.text.get("1.0", END).strip()
        if not note_content:
            messagebox.showwarning("No Note", "Please generate a note first")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if file_path:
            patient_info = self.current_patient if self.current_patient else {}
            doctor_info = self.doctor
            note_type = self.note_type_var.get()

            success = self.exporter.export_to_pdf(
                note_content,
                file_path,
                note_type=f"{note_type} Note",
                patient_info=patient_info,
                doctor_info=doctor_info
            )

            if success:
                messagebox.showinfo("Success", f"Note exported to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to export PDF")

    def export_docx(self):
        """Export note as DOCX"""
        note_content = self.note_display.text.get("1.0", END).strip()
        if not note_content:
            messagebox.showwarning("No Note", "Please generate a note first")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx")]
        )

        if file_path:
            patient_info = self.current_patient if self.current_patient else {}
            doctor_info = self.doctor
            note_type = self.note_type_var.get()

            success = self.exporter.export_to_docx(
                note_content,
                file_path,
                note_type=f"{note_type} Note",
                patient_info=patient_info,
                doctor_info=doctor_info
            )

            if success:
                messagebox.showinfo("Success", f"Note exported to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to export DOCX")

    def check_ollama_status(self):
        """Check if Ollama is running"""
        if self.llm.check_connection():
            self.ollama_status.config(
                text=" Ollama: Connected",
                bootstyle="success"
            )
        else:
            self.ollama_status.config(
                text=" Ollama: Not Connected (Start Ollama to use AI features)",
                bootstyle="danger"
            )

    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

    def run(self):
        """Start the dashboard"""
        self.root.mainloop()


class PatientDialog:
    """Dialog for adding/editing patients"""

    def __init__(self, parent, db, doctor_id, patient=None, callback=None):
        self.db = db
        self.doctor_id = doctor_id
        self.patient = patient
        self.callback = callback

        # Create dialog
        self.dialog = ttk.Toplevel(parent)
        self.dialog.title("Add Patient" if patient is None else "Edit Patient")
        self.dialog.geometry("500x550")
        self.dialog.resizable(False, False)

        # Make modal
        self.dialog.grab_set()

        self.create_form()

    def create_form(self):
        """Create patient form"""
        form_frame = ttk.Frame(self.dialog, padding=20)
        form_frame.pack(fill=BOTH, expand=YES)

        # Name
        ttk.Label(form_frame, text="Full Name *", font=("Segoe UI", 11)).pack(anchor=W, pady=(10, 5))
        self.name_entry = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.name_entry.pack(fill=X, pady=(0, 10))

        # Age
        ttk.Label(form_frame, text="Age", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.age_entry = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.age_entry.pack(fill=X, pady=(0, 10))

        # Gender
        ttk.Label(form_frame, text="Gender", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = ttk.Frame(form_frame)
        gender_frame.pack(fill=X, pady=(0, 10))
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(side=LEFT, padx=5)

        # Contact
        ttk.Label(form_frame, text="Contact", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.contact_entry = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.contact_entry.pack(fill=X, pady=(0, 10))

        # Diagnosis
        ttk.Label(form_frame, text="Diagnosis", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.diagnosis_entry = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.diagnosis_entry.pack(fill=X, pady=(0, 10))

        # ICD Code
        ttk.Label(form_frame, text="ICD Code", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.icd_entry = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.icd_entry.pack(fill=X, pady=(0, 10))

        # Notes
        ttk.Label(form_frame, text="Notes", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.notes_text = tk.Text(form_frame, height=5, font=("Segoe UI", 10))
        self.notes_text.pack(fill=X, pady=(0, 10))

        # Fill existing data if editing
        if self.patient:
            self.name_entry.insert(0, self.patient.get('name', ''))
            if self.patient.get('age'):
                self.age_entry.insert(0, str(self.patient['age']))
            if self.patient.get('gender'):
                self.gender_var.set(self.patient['gender'])
            if self.patient.get('contact'):
                self.contact_entry.insert(0, self.patient['contact'])
            if self.patient.get('diagnosis'):
                self.diagnosis_entry.insert(0, self.patient['diagnosis'])
            if self.patient.get('icd_code'):
                self.icd_entry.insert(0, self.patient['icd_code'])
            if self.patient.get('notes'):
                self.notes_text.insert("1.0", self.patient['notes'])

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=X, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="Save",
            command=self.save_patient,
            bootstyle="success",
            width=15
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bootstyle="secondary",
            width=15
        ).pack(side=LEFT, padx=5)

    def save_patient(self):
        """Save patient data"""
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning("Required Field", "Please enter patient name")
            return

        age = self.age_entry.get().strip()
        age = int(age) if age.isdigit() else None

        data = {
            'name': name,
            'age': age,
            'gender': self.gender_var.get(),
            'contact': self.contact_entry.get().strip(),
            'diagnosis': self.diagnosis_entry.get().strip(),
            'icd_code': self.icd_entry.get().strip(),
            'notes': self.notes_text.get("1.0", END).strip()
        }

        if self.patient:
            # Update existing
            success = self.db.update_patient(self.patient['id'], **data)
            msg = "Patient updated successfully"
        else:
            # Create new
            patient_id = self.db.create_patient(self.doctor_id, **data)
            success = patient_id is not None
            msg = "Patient added successfully"

        if success:
            messagebox.showinfo("Success", msg)
            if self.callback:
                self.callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to save patient")
