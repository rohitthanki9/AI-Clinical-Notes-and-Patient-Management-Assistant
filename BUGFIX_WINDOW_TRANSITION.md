# Bug Fix - Window Transition Error

## Issue Description

**Error:** `_tkinter.TclError: can't invoke "tk" command: application has been destroyed`

This error occurred when logging in successfully. The application would crash during the transition from the login window to the dashboard.

## Root Cause

The login window was being destroyed **before** the dashboard window finished initializing. This caused the Tk root to be invalidated while ttkbootstrap was still trying to apply styles to new widgets.

### Problematic Flow:
1. User clicks "Login"
2. Login window calls `self.root.destroy()` ❌
3. Callback tries to create dashboard
4. Dashboard widgets fail because Tk root is already destroyed

## Solution

Changed the window transition flow to properly handle the Tk lifecycle:

### Fixed Flow:
1. User clicks "Login"
2. Login window calls `self.root.withdraw()` ✅ (hides window)
3. Callback creates dashboard (Tk root still alive)
4. After 100ms, login window is destroyed ✅

### Code Changes

**File: `modules/gui_login.py`**

```python
# BEFORE (Broken):
if doctor:
    messagebox.showinfo("Success", f"Welcome, Dr. {doctor['name']}!")
    self.root.destroy()  # ❌ Destroys root immediately
    self.on_login_success(doctor)

# AFTER (Fixed):
if doctor:
    messagebox.showinfo("Success", f"Welcome, Dr. {doctor['name']}!")
    self.root.withdraw()  # ✅ Hide window but keep Tk alive
    self.on_login_success(doctor)  # Create dashboard
    self.root.after(100, self.root.destroy)  # ✅ Destroy after delay
```

**File: `modules/gui_dashboard.py`**

Also changed scrollbars to use standard `tk.Scrollbar` instead of `ttk.Scrollbar` to avoid ttkbootstrap style application during transitions:

```python
# Use standard tkinter scrollbar
y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
```

## How to Test

1. **Pull the latest changes:**
   ```bash
   git pull origin claude/ai-clinical-notes-app-011CUMn56nQ4QudWMRaUQVfj
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Test login:**
   - Create an account or use existing credentials
   - Click "Login"
   - You should now see the dashboard open without errors ✅

4. **Test add patient dialog:**
   - Click "Add Patient"
   - The dialog should open without the radiobutton error ✅

## Expected Behavior

- ✅ Login window closes smoothly
- ✅ Dashboard opens without errors
- ✅ All GUI elements render properly
- ✅ No TclError exceptions
- ✅ Smooth transition between windows

## Additional Notes

This is a common issue in Tkinter applications when managing multiple windows. The key is to:
1. Never destroy the root window while child widgets are being created
2. Use `withdraw()` to hide windows instead of destroying them immediately
3. Use `after()` to schedule destruction after initialization is complete

## Status

✅ **FIXED** - Commit: 2adff84

The application should now work correctly on all platforms (Windows, macOS, Linux).
