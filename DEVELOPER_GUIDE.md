# 👨‍💻 Developer Guide - Stock Manager

## 📁 Δομή Project

### Αρχεία που ΕΠΕΞΕΡΓΑΖΕΣΑΙ (Developer)

```
stock_manager/
├── app_pro.py              ⭐ ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ - Εδώ κάνεις αλλαγές
├── index.html              🌐 Website - Για αλλαγές στη σελίδα λήψης
├── requirements.txt        📦 Dependencies - Αν προσθέσεις νέες βιβλιοθήκες
└── data/
    ├── products.json       📊 Template προϊόντων
    ├── movements.json      📝 Template κινήσεων
    └── categories.json     📂 Κατηγορίες
```

### Αρχεία που ΔΕΝ αλλάζεις (Auto-generated)

```
❌ dist/                    (Δημιουργείται με build_exe.py)
❌ build/                   (Temp PyInstaller files)
❌ __pycache__/            (Python cache)
❌ *.zip                   (Release packages)
❌ .venv/                  (Virtual environment)
```

---

## 🔧 Workflow Ανάπτυξης

### 1️⃣ Κάνε Αλλαγές στον Κώδικα

#### Για αλλαγές στο πρόγραμμα:
```bash
# Άνοιξε το app_pro.py
code app_pro.py

# Κάνε τις αλλαγές σου
# Π.χ.: Πρόσθεσε νέο feature, διόρθωσε bug, κλπ
```

#### Για αλλαγές στο website:
```bash
# Άνοιξε το index.html
code index.html

# Αλλαγές: χρώματα, κείμενα, links, κλπ
```

---

### 2️⃣ Test Τοπικά

```bash
# Τρέξε το πρόγραμμα για test
python app_pro.py

# Αν έχει bugs, διόρθωσε και ξανά-τεστάρισε
```

---

### 3️⃣ Ενημέρωσε την Έκδοση

```bash
# Άνοιξε το VERSION file
code VERSION

# Άλλαξε από 1.0.0 σε 1.1.0 (ή 1.0.1 για bugfix)
```

#### Versioning Rules:
- **1.0.0 → 1.0.1**: Bugfix (μικρή διόρθωση)
- **1.0.0 → 1.1.0**: New feature (νέο χαρακτηριστικό)
- **1.0.0 → 2.0.0**: Breaking change (μεγάλη αλλαγή)

---

### 4️⃣ Build νέο EXE

```bash
# Δημιούργησε το νέο εκτελέσιμο
python build_exe.py

# Θα δημιουργηθεί: dist/StockManager.exe
```

---

### 5️⃣ Δημιούργησε Release Package

```powershell
# Τρέξε το release script
.\create_release.ps1

# Θα δημιουργηθεί: StockManager_v1.1.0.zip
```

---

### 6️⃣ Commit στο Git

```bash
# Stage όλες τις αλλαγές
git add .

# Commit με περιγραφικό μήνυμα
git commit -m "v1.1.0 - Added dark mode feature"

# Push στο GitHub
git push
```

---

### 7️⃣ Δημιούργησε GitHub Release

#### Βήμα 1: Ανέβασε το ZIP στο Google Drive
1. Upload: `StockManager_v1.1.0.zip`
2. Share → "Anyone with the link"
3. Αντίγραψε το link

#### Βήμα 2: Δημιούργησε Release
1. Πήγαινε: https://github.com/Mimisnak/stock-manager/releases/new
2. **Tag**: `v1.1.0`
3. **Title**: `Stock Manager v1.1.0 - [Όνομα Feature]`
4. **Description**:
```markdown
## Νέα Έκδοση v1.1.0

### Νέα Χαρακτηριστικά
- ✨ [Feature 1]
- ✨ [Feature 2]

### Διορθώσεις
- 🐛 [Bug fix 1]
- 🐛 [Bug fix 2]

### Λήψη
[Κατέβασε από Google Drive](YOUR_DRIVE_LINK)

---
Για να ενημερώσεις:
1. Κατέβασε το νέο ZIP
2. Αντικατέστησε μόνο το StockManager.exe
3. Κράτα τον φάκελο data/ (έχει τα δεδομένα σου)
```

5. Πάτα **Publish release**

---

### 8️⃣ Ενημέρωσε το index.html (αν χρειάζεται)

```bash
# Άνοιξε το index.html
code index.html

# Άλλαξε:
# - Version badge: v1.0.0 → v1.1.0
# - Changelog: Πρόσθεσε τη νέα έκδοση
# - Download link: Ενημέρωσε αν άλλαξε

# Commit & Push
git add index.html
git commit -m "Update website for v1.1.0"
git push
```

---

## 📝 Checklist για Κάθε Release

```
[ ] 1. Έκανες όλες τις αλλαγές στο app_pro.py
[ ] 2. Τέσταρες τοπικά (python app_pro.py)
[ ] 3. Ενημέρωσες το VERSION file
[ ] 4. Build EXE (python build_exe.py)
[ ] 5. Δημιούργησες ZIP (.\create_release.ps1)
[ ] 6. Τέσταρες το EXE από το ZIP
[ ] 7. Commit & Push στο Git
[ ] 8. Upload ZIP στο Google Drive
[ ] 9. Δημιούργησες GitHub Release
[ ] 10. Ενημέρωσες index.html (αν χρειάζεται)
```

---

## 🎯 Συχνές Αλλαγές

### Πρόσθεσε νέο Feature

```python
# Στο app_pro.py, βρες το section που θες
# Πχ για νέο button:

def new_feature_button(self):
    btn = ttk.Button(self.parent_frame, text="Νέο Feature", 
                     command=self.new_feature_action)
    btn.pack()

def new_feature_action(self):
    # Η λογική του feature
    messagebox.showinfo("Feature", "Το νέο feature!")
```

### Άλλαξε χρώματα στο GUI

```python
# Στο app_pro.py, βρες το configure_styles()
style = ttk.Style()
style.configure("Custom.TButton", background="#00ff41")
```

### Άλλαξε χρώματα στο Website

```html
<!-- Στο index.html, section <style> -->
body {
    background: #0a0e27;  /* Αλλαγή background */
}

.download-btn {
    background: #00ff41;  /* Αλλαγή κουμπιού */
}
```

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Εγκατέστησε τις dependencies
pip install -r requirements.txt
```

### EXE δεν δουλεύει
```bash
# Έλεγξε το build
python build_exe.py

# Δες το output για errors
```

### Git conflicts
```bash
# Pull πρώτα
git pull

# Resolve conflicts
# Μετά commit & push
```

---

## 💡 Tips

1. **Πάντα test πριν το release!**
2. **Κράτα backups του working code**
3. **Γράψε περιγραφικά commit messages**
4. **Version bumps: Bugfix → 0.0.X, Feature → 0.X.0, Breaking → X.0.0**
5. **Ενημέρωσε το README με νέα features**

---

## 🔗 Quick Links

- **Repository**: https://github.com/Mimisnak/stock-manager
- **Releases**: https://github.com/Mimisnak/stock-manager/releases
- **Website**: https://mimisnak.github.io/stock-manager/
- **Your Site**: https://mimis.dev

---

## 📞 Support

Αν κολλήσεις, άνοιξε Issue στο GitHub ή στείλε μήνυμα!

---

**Happy Coding! 🚀**
