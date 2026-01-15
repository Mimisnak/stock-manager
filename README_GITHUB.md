# 📦 Stock Manager - Professional Edition

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.13-green.svg)
![License](https://img.shields.io/badge/license-Free-brightgreen.svg)

**Επαγγελματικό Σύστημα Διαχείρισης Αποθέματος με GUI**

[🌐 Σελίδα Λήψης](https://mimisnak.github.io/stock-manager/) • [📦 Releases](https://github.com/Mimisnak/stock-manager/releases) • [🐛 Issues](https://github.com/Mimisnak/stock-manager/issues)

</div>

---

## ⚡ Quick Start (για χρήστες)

**Κατέβασε το EXE έτοιμο προς χρήση:**

1. Πήγαινε στο [Releases](https://github.com/Mimisnak/stock-manager/releases/latest)
2. Κατέβασε το `StockManager.zip`
3. Αποσυμπίεσε και τρέξε το `StockManager.exe`
4. Έτοιμο! 🎉

**Δεν χρειάζεται Python ή εγκατάσταση βιβλιοθηκών!**

---

## ✨ Χαρακτηριστικά

### 📊 Core Features
- ✅ **Διαχείριση Προϊόντων**: Προσθήκη, επεξεργασία, διαγραφή με πλήρη στοιχεία
- ✅ **Live Dashboard**: Στατιστικά σε πραγματικό χρόνο με auto-refresh κάθε 30"
- ✅ **Κινήσεις Αποθέματος**: Παρακολούθηση εισόδων/εξόδων με timestamps
- ✅ **Κατηγορίες**: 10+ προκαθορισμένες κατηγορίες με emojis
- ✅ **126 Προεγκατεστημένα Προϊόντα**: Πίτσες, Σφολιάτες, Μπουγάτσες, κλπ

### 📄 Εξαγωγές & Reports
- ✅ **PDF Export**: Επαγγελματικά reports με πίνακες
- ✅ **Excel Export**: 3 sheets (Προϊόντα, Κινήσεις, Απόθεμα)
- ✅ **Υποστήριξη Ελληνικών**: Πλήρης υποστήριξη ελληνικών χαρακτήρων

### 💾 Ασφάλεια Δεδομένων
- ✅ **Auto-Save**: Αυτόματη αποθήκευση σε κάθε αλλαγή
- ✅ **Auto-Backup**: 20 τελευταία backups με rotation
- ✅ **Manual Backup/Restore**: Χειροκίνητα backups με timestamps
- ✅ **Safe Exit**: Επιβεβαίωση πριν το κλείσιμο με final backup

### 🔍 Αναζήτηση & Φίλτρα
- ✅ **Real-time Search**: Αναζήτηση σε όλα τα πεδία
- ✅ **Category Filters**: Φιλτράρισμα ανά κατηγορία
- ✅ **Status Filters**: Χαμηλό απόθεμα, ΟΚ, Υπερβολικό

### ⚠️ Ειδοποιήσεις
- ✅ **Low Stock Alerts**: Αυτόματες ειδοποιήσεις χαμηλού αποθέματος
- ✅ **Window Title Stats**: Live στατιστικά στον τίτλο παραθύρου
- ✅ **Color Coded**: Χρωματική κωδικοποίηση για γρήγορη αναγνώριση

---

## 💻 Τεχνικές Λεπτομέρειες

### Τεχνολογίες
- **Python**: 3.13
- **GUI**: tkinter/ttk με custom styling
- **Data**: JSON για persistence
- **PDF**: reportlab
- **Excel**: pandas + openpyxl

### Αρχιτεκτονική
```
stock_manager/
├── app_pro.py              # Main application (2000+ lines)
├── data/
│   ├── products.json       # Προϊόντα με όλα τα στοιχεία
│   ├── movements.json      # Ιστορικό κινήσεων
│   ├── categories.json     # Κατηγορίες με emojis
│   └── backups/           # Auto backups (20 rotation)
├── build_exe.py           # PyInstaller build script
├── create_release.ps1     # Release automation
└── index.html            # GitHub Pages landing page
```

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.13+
- Git
- Windows 10/11

### Installation

```bash
# Clone repository
git clone https://github.com/Mimisnak/stock-manager.git
cd stock-manager

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app_pro.py
```

### Build EXE

```bash
# Install PyInstaller
pip install pyinstaller

# Build standalone EXE
python build_exe.py

# Output: dist/StockManager.exe (~54 MB)
```

### Create Release Package

```powershell
# PowerShell script
.\create_release.ps1

# Creates: StockManager_v1.0.0.zip
```

---

## 📦 Απαιτήσεις Συστήματος

### Για Χρήστες (EXE)
- ✅ Windows 10 ή νεότερο (64-bit)
- ✅ 100 MB ελεύθερος χώρος
- ✅ 2 GB RAM
- ✅ Οθόνη 1024x768+
- ❌ **Δεν** χρειάζεται Python

### Για Developers
- Python 3.13+
- pip packages: `tkinter`, `pandas`, `openpyxl`, `reportlab`
- PyInstaller για build

---

## 🚀 Roadmap

### v1.1.0 (Planned)
- [ ] Dark Mode theme
- [ ] Multi-language support (EN, EL)
- [ ] Database export (SQLite)
- [ ] Advanced filters & sorting

### v1.2.0 (Future)
- [ ] Cloud backup (Google Drive, OneDrive)
- [ ] Email notifications
- [ ] Barcode scanning support
- [ ] Multi-user support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 Changelog

### v1.0.0 (2026-01-15) - Initial Release
- 🎉 First public release
- ✅ Complete stock management system
- ✅ 126 pre-loaded products
- ✅ PDF & Excel exports
- ✅ Auto-backup system
- ✅ Greek language support
- ✅ Live dashboard with auto-refresh

---

## 🐛 Αναφορά Προβλημάτων

Βρήκες bug; Θέλεις νέο feature;

1. Έλεγξε αν υπάρχει ήδη [Issue](https://github.com/Mimisnak/stock-manager/issues)
2. Αν όχι, [δημιούργησε νέο](https://github.com/Mimisnak/stock-manager/issues/new)
3. Περίγραψε το πρόβλημα με screenshots

---

## 📄 License

Αυτό το project είναι **free** και διατίθεται ελεύθερα για χρήση.

---

## 👨‍💻 Author

**Mimisnak**
- GitHub: [@Mimisnak](https://github.com/Mimisnak)
- Repository: [stock-manager](https://github.com/Mimisnak/stock-manager)

---

## ⭐ Support

Αν σου αρέσει αυτό το project, δώσε ένα ⭐ στο GitHub!

---

<div align="center">

**Developed with ❤️ for professional stock management**

[🌐 Website](https://mimisnak.github.io/stock-manager/) • [📦 Download](https://github.com/Mimisnak/stock-manager/releases/latest) • [📖 Docs](https://github.com/Mimisnak/stock-manager/blob/main/README_USERS.md)

</div>
