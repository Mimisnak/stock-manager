"""
Script για δημιουργία standalone EXE του Stock Manager
Τρέχει PyInstaller με τις σωστές παραμέτρους
"""
import subprocess
import sys
from pathlib import Path

def build_exe():
    """Δημιουργεί το EXE με PyInstaller"""
    
    print("🔨 Δημιουργία EXE αρχείου...")
    print("=" * 60)
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=StockManager",           # Όνομα exe
        "--onefile",                      # Ένα μόνο exe αρχείο
        "--windowed",                     # Χωρίς console window
        "--icon=NONE",                    # Μπορείς να προσθέσεις icon μετά
        "--add-data=data;data",           # Συμπερίληψη φακέλου data
        "--hidden-import=PIL",            # Για reportlab
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.pdfgen",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=reportlab.platypus",
        "--hidden-import=openpyxl",
        "--hidden-import=pandas",
        "--clean",                        # Καθαρισμός πριν το build
        "app_pro.py"                      # Το main script
    ]
    
    try:
        # Εκτέλεση PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("\n✅ ΕΠΙΤΥΧίΑ!")
        print("=" * 60)
        print(f"📦 Το EXE δημιουργήθηκε στο: dist\\StockManager.exe")
        print(f"📊 Μέγεθος: ~{Path('dist/StockManager.exe').stat().st_size / (1024*1024):.1f} MB")
        print("\n📝 Οδηγίες διανομής:")
        print("   1. Το EXE βρίσκεται στον φάκελο 'dist'")
        print("   2. Αντέγραψε ΚΑΙ το EXE ΚΑΙ τον φάκελο 'data' μαζί")
        print("   3. Μοίρασε και τα δύο στους χρήστες")
        print("   4. Οι χρήστες τρέχουν μόνο το StockManager.exe")
        print("\n🔒 Ασφάλεια:")
        print("   ✓ Ο κώδικας είναι μεταγλωττισμένος (compiled)")
        print("   ✓ Δεν μπορούν να δουν/αλλάξουν τον Python κώδικα")
        print("   ✓ Για updates, στείλε νέο EXE")
        
    except subprocess.CalledProcessError as e:
        print("\n❌ ΣΦΑΛΜΑ κατά το build:")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ ΣΦΑΛΜΑ: Το PyInstaller δεν βρέθηκε!")
        print("Τρέξε πρώτα: pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
