# Script for automatic release package creation
# Run this before making a GitHub release

$ErrorActionPreference = "Stop"

Write-Host "Creating Release Package for Stock Manager" -ForegroundColor Cyan
Write-Host ("=" * 60)

# Read version
$version = Get-Content "VERSION" -Raw
$version = $version.Trim()
Write-Host "Version: v$version" -ForegroundColor Yellow

# Create release folder
$releaseName = "StockManager_v$version"
$releaseDir = "release_temp"

Write-Host "`nCleaning old releases..." -ForegroundColor Gray
if (Test-Path $releaseDir) {
    Remove-Item $releaseDir -Recurse -Force
}
New-Item -ItemType Directory -Path $releaseDir -Force | Out-Null

Write-Host "Copying files..." -ForegroundColor Gray

# Δημιουργία δομής
$targetDir = Join-Path $releaseDir "StockManager"
New-Item -ItemType Directory -Path $targetDir -Force | Out-Null

# Αντιγραφή EXE
if (Test-Path "dist\StockManager.exe") {
    Copy-Item "dist\StockManager.exe" $targetDir
    Write-Host "  [OK] StockManager.exe" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] EXE not found! Run first: python build_exe.py" -ForegroundColor Red
    exit 1
}

# Αντιγραφή data folder
if (Test-Path "data") {
    Copy-Item "data" $targetDir -Recurse -Force
    Write-Host "  [OK] data/" -ForegroundColor Green
} else {
    Write-Host "  [WARNING] data/ not found" -ForegroundColor Yellow
}

# Αντιγραφή README
if (Test-Path "README_USERS.md") {
    Copy-Item "README_USERS.md" $targetDir
    Write-Host "  [OK] README_USERS.md" -ForegroundColor Green
}

# Δημιουργία ZIP
$zipName = "$releaseName.zip"
Write-Host "`nCompressing to ZIP..." -ForegroundColor Gray

if (Test-Path $zipName) {
    Remove-Item $zipName -Force
}

Compress-Archive -Path "$targetDir\*" -DestinationPath $zipName -CompressionLevel Optimal

# Υπολογισμός μεγέθους
$zipSize = (Get-Item $zipName).Length / 1MB

Write-Host "`nSUCCESS!" -ForegroundColor Green
Write-Host ("=" * 60)
Write-Host "Created: $zipName" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Go to GitHub -> Releases -> New Release"
Write-Host "  2. Tag: v$version"
Write-Host "  3. Title: Stock Manager v$version"
Write-Host "  4. Attach file: $zipName"
Write-Host "  5. Publish release"
Write-Host "`nThen, update index.html if needed"

# Καθαρισμός temp folder
Remove-Item $releaseDir -Recurse -Force
Write-Host "`nTemp files cleared" -ForegroundColor Gray
