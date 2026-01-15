# 🚀 Quick Reference - Developer Cheat Sheet

## Γρήγορες Εντολές

### Κάνε Αλλαγές & Release

```bash
# 1. Κάνε αλλαγές στο app_pro.py
code app_pro.py

# 2. Test
python app_pro.py

# 3. Ενημέρωσε version
echo "1.1.0" > VERSION

# 4. Build EXE
python build_exe.py

# 5. Create ZIP
.\create_release.ps1

# 6. Git commit
git add .
git commit -m "v1.1.0 - Description"
git push

# 7. Create GitHub Release με το ZIP
```

---

## Αρχεία που Επεξεργάζεσαι

| Αρχείο | Πότε | Για τι |
|---------|------|--------|
| `app_pro.py` | Πάντα | Κύριο πρόγραμμα |
| `index.html` | Σπάνια | Website αλλαγές |
| `VERSION` | Κάθε release | Αριθμός έκδοσης |
| `requirements.txt` | Αν προσθέσεις lib | Dependencies |

---

## Version Numbers

- **1.0.0 → 1.0.1** = Bugfix
- **1.0.0 → 1.1.0** = New Feature  
- **1.0.0 → 2.0.0** = Breaking Change

---

## Git Commands

```bash
# Status
git status

# Commit όλα
git add .
git commit -m "Your message"
git push

# Νέο branch
git checkout -b feature-name

# Merge
git checkout main
git merge feature-name
```

---

## PyInstaller Options

```bash
# Στο build_exe.py:
--onefile          # Ένα EXE
--windowed        # Χωρίς console
--add-data        # Προσθήκη files
--hidden-import   # Extra modules
```

---

## Troubleshooting

| Πρόβλημα | Λύση |
|----------|------|
| Module not found | `pip install -r requirements.txt` |
| EXE crash | Check console: `python app_pro.py` |
| Git conflict | `git pull` → resolve → commit |
| Big ZIP | Χρήση Google Drive |

---

## 📍 Bookmarks

- [Repo](https://github.com/Mimisnak/stock-manager)
- [Releases](https://github.com/Mimisnak/stock-manager/releases)
- [Website](https://mimisnak.github.io/stock-manager/)
