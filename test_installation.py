#!/usr/bin/env python3
"""
Installation Test Script
Verifies all dependencies and components are properly installed
"""

import sys
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print("Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"OK (Python {version.major}.{version.minor}.{version.micro})")
        return True
    else:
        print(f"FAIL (Need Python 3.8+, found {version.major}.{version.minor})")
        return False

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    display_name = package_name or module_name
    print(f"Testing {display_name}...", end=" ")
    try:
        __import__(module_name)
        print("OK")
        return True
    except ImportError as e:
        print(f"FAIL ({e})")
        return False

def test_ollama():
    """Test Ollama connection"""
    print("Testing Ollama connection...", end=" ")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("OK")
            # Check for llama3 model
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            if any('llama3' in m.lower() for m in models):
                print("  Llama3 model: Found")
            else:
                print("  WARNING: Llama3 model not found. Run: ollama pull llama3")
            return True
        else:
            print("FAIL (Unable to connect)")
            return False
    except Exception as e:
        print(f"FAIL ({e})")
        print("  Make sure Ollama is running!")
        return False

def test_directories():
    """Test required directories"""
    print("Testing directory structure...", end=" ")
    required = ['modules', 'prompts', 'data', 'assets']
    missing = []
    for dir_name in required:
        if not Path(dir_name).exists():
            missing.append(dir_name)

    if missing:
        print(f"FAIL (Missing: {', '.join(missing)})")
        return False
    else:
        print("OK")
        return True

def test_modules():
    """Test custom modules"""
    print("Testing custom modules...", end=" ")
    modules = [
        'modules.config_manager',
        'modules.patient_db',
        'modules.encryption_manager',
        'modules.icd_lookup',
        'modules.speech_to_text',
        'modules.llm_processing_ollama',
        'modules.note_formatter',
        'modules.export_manager',
        'modules.gui_login',
        'modules.gui_dashboard'
    ]

    failed = []
    for module in modules:
        try:
            __import__(module)
        except Exception as e:
            failed.append(f"{module}: {e}")

    if failed:
        print("FAIL")
        for f in failed:
            print(f"  {f}")
        return False
    else:
        print("OK")
        return True

def main():
    """Run all tests"""
    print("=" * 70)
    print("AI Clinical Notes - Installation Test".center(70))
    print("=" * 70)
    print()

    tests = [
        ("Python Version", test_python_version),
        ("Tkinter", lambda: test_import("tkinter")),
        ("ttkbootstrap", lambda: test_import("ttkbootstrap")),
        ("Whisper", lambda: test_import("whisper", "openai-whisper")),
        ("sounddevice", lambda: test_import("sounddevice")),
        ("soundfile", lambda: test_import("soundfile")),
        ("numpy", lambda: test_import("numpy")),
        ("requests", lambda: test_import("requests")),
        ("python-docx", lambda: test_import("docx", "python-docx")),
        ("reportlab", lambda: test_import("reportlab")),
        ("cryptography", lambda: test_import("cryptography")),
        ("Directories", test_directories),
        ("Custom Modules", test_modules),
        ("Ollama", test_ollama)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"ERROR during {name} test: {e}")
            results.append((name, False))
        print()

    # Summary
    print("=" * 70)
    print("Summary".center(70))
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n ALL TESTS PASSED! ")
        print("\nYou're ready to run the application:")
        print("  python main.py")
    else:
        print("\n SOME TESTS FAILED ")
        print("\nFailed tests:")
        for name, result in results:
            if not result:
                print(f"  - {name}")
        print("\nPlease fix the issues above before running the application.")
        print("See SETUP_GUIDE.md for help.")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
