# 🚀 Οδηγίες Ανεβάσματος στο GitHub

## 📋 Προετοιμασία

### 1. Δημιούργησε Repository στο GitHub

1. Πήγαινε στο https://github.com
2. Κάνε login
3. Πάτα το **+** (πάνω δεξιά) → **New repository**
4. Όνομα: `stock-manager`
5. Description: `Professional Stock Management System with GUI`
6. **Public** (για να λειτουργήσει το GitHub Pages)
7. ✅ **ΜΗΝ** προσθέσεις README, .gitignore, ή license (τα έχουμε ήδη)
8. Πάτα **Create repository**

---

## 💻 Ανέβασμα Κώδικα

### Άνοιξε PowerShell στον φάκελο `stock_manager` και τρέξε:

```powershell
# 1. Initialize Git
git init

# 2. Προσθήκη όλων των αρχείων
git add .

# 3. Πρώτο commit
git commit -m "Initial commit - Stock Manager v1.0.0"

# 4. Σύνδεση με το GitHub repository
git remote add origin https://github.com/Mimisnak/stock-manager.git

# 5. Rename branch σε main
git branch -M main

# 6. Push στο GitHub
git push -u origin main
```

---

## 🌐 Ενεργοποίηση GitHub Pages

### Στο GitHub repository σου:

1. Πήγαινε στο **Settings** (δεξιά πάνω)
2. Αριστερά μενού → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** / folder: **/ (root)**
5. Πάτα **Save**

✅ Μετά από 1-2 λεπτά, η σελίδα σου θα είναι live στο:
```
https://YOUR_USERNAME.github.io/stock-manager/
```

---

## 📦 Δημιουργία Release με το EXE

### 1. Συμπίεσε το EXE

```powershell
# Δημιούργησε φάκελο για διανομή
New-Item -ItemType Directory -Path "StockManager_Release" -Force

# Αντίγραψε τα απαραίτητα αρχεία
Copy-Item "dist\StockManager.exe" "StockManager_Release\"
Copy-Item "data\" "StockManager_Release\data\" -Recurse
Copy-Item "README_USERS.md" "StockManager_Release\"

# Συμπίεση σε ZIP
Compress-Archive -Path "StockManager_Release\*" -DestinationPath "StockManager.zip" -Force

Write-Host "✅ StockManager.zip δημιουργήθηκε!"
```

### 2. Upload στο GitHub Releases

1. Στο GitHub repository → **Releases** (δεξιά)
2. Πάτα **Create a new release**
3. **Tag version**: `v1.0.0`
4. **Release title**: `Stock Manager v1.0.0 - Initial Release`
5. **Description**:
```markdown
## 🎉 Αρχική Κυκλοφορία

### ✨ Χαρακτηριστικά
- ✅ Πλήρες σύστημα διαχείρισης αποθέματος
- ✅ 126 προεγκατεστημένα προϊόντα
- ✅ Live Dashboard με auto-refresh
- ✅ Εξαγωγή PDF & Excel
- ✅ Αυτόματα backups
- ✅ Υποστήριξη ελληνικών

### 📥 Λήψη
Κατέβασε το `StockManager.zip` παρακάτω

### 📖 Οδηγίες
Δες το [README_USERS.md](https://github.com/Mimisnak/stock-manager/blob/main/README_USERS.md)

---
💾 Μέγεθος: ~20 MB | 💻 Windows 10/11 | 🆓 Δωρεάν
```

6. **Attach files**: Σύρε το `StockManager.zip`
7. Πάτα **Publish release**

---

## 🔄 Για Μελλοντικές Ενημερώσεις

### Όταν κάνεις αλλαγές στον κώδικα:

```powershell
# 1. Άλλαξε το VERSION file
"1.1.0" | Out-File -FilePath "VERSION" -Encoding UTF8 -NoNewline

# 2. Ενημέρωσε το index.html (άλλαξε το v1.0.0 σε v1.1.0)

# 3. Build νέο EXE
python build_exe.py

# 4. Git commit & push
git add .
git commit -m "Update to v1.1.0 - Added new features"
git push

# 5. Δημιούργησε νέο ZIP και Release
# (Επανέλαβε τα βήματα από πάνω)
```

---

## 📝 Checklist Πριν το Push

- ✅ `.gitignore` έτοιμο
- ✅ `README.md` ενημερωμένο
- ✅ `requirements.txt` έχει όλες τις dependencies
- ✅ `index.html` με σωστό username
- ✅ `VERSION` file με τρέχουσα έκδοση
- ✅ Data folder χωρίς ευαίσθητα δεδομένα
- ✅ EXE built και tested

---

## 🔗 Σημαντικά URLs

**Στο index.html άλλαξε:**
- `Mimisnak` → το GitHub username σου
- Email στο Support section
- Οποιαδήποτε άλλα links

**Το repository URL θα είναι:**
```
https://github.com/Mimisnak/stock-manager
```

**Η σελίδα λήψης θα είναι:**
```
https://Mimisnak.github.io/stock-manager/
```

---

## 🎯 Έτοιμο!

Τώρα οι χρήστες μπορούν:
1. Να επισκεφτούν την HTML σελίδα σου
2. Να κατεβάσουν το EXE από Releases
3. Να βλέπουν αυτόματα ειδοποιήσεις για νέες εκδόσεις!

---

## 💡 Pro Tips

- Κάνε **tag** κάθε release (`v1.0.0`, `v1.1.0`, etc.)
- Γράφε **changelog** σε κάθε release
- Κράτα **semantic versioning**: `MAJOR.MINOR.PATCH`
- Τέσταρε το EXE πριν το release
- Κράτα backups των ZIP files
