# 🍎 Οδηγίες εγκατάστασης για Mac & Linux

## Προαπαιτούμενα
- Python 3.8 ή νεότερο
- pip (Python package installer)

## Βήματα εγκατάστασης

### 1. Κατέβασε τον κώδικα
```bash
# Κατέβασε το ZIP από το GitHub και το αποσυμπιέζεις
# Ή κάνε clone το repository:
git clone https://github.com/Mimisnak/stock-manager.git
cd stock-manager
```

### 2. Εγκατάσταση εξαρτήσεων
```bash
pip install -r requirements.txt
```

### 3. Εκτέλεση της εφαρμογής
```bash
python app_pro.py
```

## Troubleshooting

### Αν δεν έχεις Python:
**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Linux (CentOS/RHEL/Fedora):**
```bash
sudo dnf install python3 python3-pip
# ή για παλαιότερα συστήματα: sudo yum install python3 python3-pip
```

**Linux (Arch):**
```bash
sudo pacman -S python python-pip
```

### Αν δεν βρεις το requirements.txt:
Εγκατάστησε τις απαραίτητες βιβλιοθήκες χειροκίνητα:
```bash
pip install pandas openpyxl matplotlib pillow pyzbar qrcode reportlab

# Επιπλέον, εγκατάστησε το tkinter:
# Mac
brew install python-tk

# Linux (Ubuntu/Debian)
sudo apt-get install python3-tk

# Linux (CentOS/RHEL/Fedora)
sudo dnf install python3-tkinter

# Linux (Arch)
sudo pacman -S tk
```

## Ερωτήσεις;
Άνοιξε ένα issue στο GitHub!
