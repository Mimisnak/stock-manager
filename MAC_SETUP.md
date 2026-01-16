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

### Αν δεν έχεις το requirements.txt:
Εγκατάστησε μόνο το tkinter:
```bash
# Mac
brew install python-tk

# Linux
sudo apt-get install python3-tk
```

## Ερωτήσεις;
Άνοιξε ένα issue στο GitHub!
