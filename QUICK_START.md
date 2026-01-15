# Οδηγίες Git Push - Γρήγορο Setup

## Βήμα 1: Δημιούργησε Repository στο GitHub
1. Πήγαινε: https://github.com/new
2. Repository name: `stock-manager`
3. Public ✅
4. Create repository

## Βήμα 2: Τρέξε αυτές τις εντολές

```powershell
# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit - Stock Manager v1.0.0"

# Add remote
git remote add origin https://github.com/Mimisnak/stock-manager.git

# Rename to main
git branch -M main

# Push
git push -u origin main
```

## Βήμα 3: GitHub Pages
1. Πήγαινε: Settings → Pages
2. Source: main branch / root folder
3. Save

✅ Η σελίδα σου: https://Mimisnak.github.io/stock-manager/

## Βήμα 4: Create Release
1. GitHub → Releases → New Release
2. Tag: v1.0.0
3. Title: Stock Manager v1.0.0
4. Upload: StockManager_v1.0.0.zip (που δημιούργησες)
5. Publish

Τέλειωσες! 🎉
