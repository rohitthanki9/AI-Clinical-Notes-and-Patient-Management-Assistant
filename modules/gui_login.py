"""
Login GUI for AI Clinical Notes Assistant
Handles doctor login and signup
"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class LoginWindow:
    def __init__(self, db_manager, on_login_success):
        """
        Initialize login window
        Args:
            db_manager: PatientDatabase instance
            on_login_success: Callback function when login successful
        """
        self.db = db_manager
        self.on_login_success = on_login_success

        # Create main window
        self.root = ttk.Window(themename="flatly")
        self.root.title("AI Clinical Notes - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Center window
        self.center_window()

        # Create UI
        self.create_login_ui()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_login_ui(self):
        """Create login/signup interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill=BOTH, expand=YES)

        # Logo/Title area
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(0, 30))

        title_label = ttk.Label(
            title_frame,
            text="AI Clinical Notes",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Patient Management Assistant",
            font=("Segoe UI", 12),
            bootstyle="secondary"
        )
        subtitle_label.pack()

        # Notebook for Login/Signup tabs
        self.notebook = ttk.Notebook(main_frame, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)

        # Login tab
        login_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(login_tab, text="Login")
        self.create_login_tab(login_tab)

        # Signup tab
        signup_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(signup_tab, text="Sign Up")
        self.create_signup_tab(signup_tab)

    def create_login_tab(self, parent):
        """Create login form"""
        # Email field
        ttk.Label(parent, text="Email:", font=("Segoe UI", 11)).pack(anchor=W, pady=(10, 5))
        self.login_email = ttk.Entry(parent, font=("Segoe UI", 11), width=35)
        self.login_email.pack(pady=(0, 15))

        # Password field
        ttk.Label(parent, text="Password:", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.login_password = ttk.Entry(parent, show="*", font=("Segoe UI", 11), width=35)
        self.login_password.pack(pady=(0, 20))

        # Bind Enter key
        self.login_email.bind('<Return>', lambda e: self.login_password.focus())
        self.login_password.bind('<Return>', lambda e: self.handle_login())

        # Login button
        login_btn = ttk.Button(
            parent,
            text="Login",
            command=self.handle_login,
            bootstyle="primary",
            width=20
        )
        login_btn.pack(pady=10)

        # Info label
        info_label = ttk.Label(
            parent,
            text="Don't have an account? Use the Sign Up tab",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        )
        info_label.pack(pady=20)

    def create_signup_tab(self, parent):
        """Create signup form"""
        # Name field
        ttk.Label(parent, text="Full Name:", font=("Segoe UI", 11)).pack(anchor=W, pady=(10, 5))
        self.signup_name = ttk.Entry(parent, font=("Segoe UI", 11), width=35)
        self.signup_name.pack(pady=(0, 15))

        # Email field
        ttk.Label(parent, text="Email:", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.signup_email = ttk.Entry(parent, font=("Segoe UI", 11), width=35)
        self.signup_email.pack(pady=(0, 15))

        # Password field
        ttk.Label(parent, text="Password:", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.signup_password = ttk.Entry(parent, show="*", font=("Segoe UI", 11), width=35)
        self.signup_password.pack(pady=(0, 15))

        # Confirm password field
        ttk.Label(parent, text="Confirm Password:", font=("Segoe UI", 11)).pack(anchor=W, pady=(0, 5))
        self.signup_confirm = ttk.Entry(parent, show="*", font=("Segoe UI", 11), width=35)
        self.signup_confirm.pack(pady=(0, 20))

        # Bind Enter key
        self.signup_name.bind('<Return>', lambda e: self.signup_email.focus())
        self.signup_email.bind('<Return>', lambda e: self.signup_password.focus())
        self.signup_password.bind('<Return>', lambda e: self.signup_confirm.focus())
        self.signup_confirm.bind('<Return>', lambda e: self.handle_signup())

        # Signup button
        signup_btn = ttk.Button(
            parent,
            text="Create Account",
            command=self.handle_signup,
            bootstyle="success",
            width=20
        )
        signup_btn.pack(pady=10)

    def handle_login(self):
        """Handle login attempt"""
        email = self.login_email.get().strip()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showwarning("Input Required", "Please enter both email and password")
            return

        # Attempt authentication
        doctor = self.db.authenticate_doctor(email, password)

        if doctor:
            messagebox.showinfo("Success", f"Welcome, Dr. {doctor['name']}!")
            # Hide the login window instead of destroying it
            self.root.withdraw()
            # Call the callback to create dashboard
            self.on_login_success(doctor)
            # Now destroy the login window after dashboard is created
            self.root.after(100, self.root.destroy)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
            self.login_password.delete(0, END)

    def handle_signup(self):
        """Handle signup attempt"""
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()

        # Validation
        if not all([name, email, password, confirm]):
            messagebox.showwarning("Input Required", "Please fill in all fields")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            self.signup_confirm.delete(0, END)
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        if '@' not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        # Attempt to create account
        doctor_id = self.db.create_doctor(name, email, password)

        if doctor_id:
            messagebox.showinfo(
                "Success",
                "Account created successfully! You can now log in."
            )
            # Switch to login tab and populate email
            self.notebook.select(0)
            self.login_email.delete(0, END)
            self.login_email.insert(0, email)
            self.login_password.focus()

            # Clear signup fields
            self.signup_name.delete(0, END)
            self.signup_email.delete(0, END)
            self.signup_password.delete(0, END)
            self.signup_confirm.delete(0, END)
        else:
            messagebox.showerror(
                "Error",
                "Email already exists. Please use a different email or log in."
            )

    def run(self):
        """Start the login window"""
        self.root.mainloop()
