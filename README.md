# 🏪 Stock Manager - Inventory System

Σύστημα διαχείρισης αποθήκης που αναπαράγει τη λογική του Excel inventory αρχείου.

## 📋 Περιγραφή

Το σύστημα διαβάζει το Excel αρχείο `e56eac39-216f-413c-a208-f99c6bb26051.xlsx` και:

- Φορτώνει τη **ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ** (προϊόντα, κωδικοί, αρχικό απόθεμα, ελάχιστα όρια)
- Επεξεργάζεται τις **ΚΙΝΗΣΕΙΣ** (εισαγωγές/εξαγωγές)
- Υπολογίζει το **ΑΠΟΘΕΜΑ** (τρέχον απόθεμα, κατάσταση)
- Εντοπίζει και αναφέρει **ERRORS** (λάθη σε κινήσεις)

## 🚀 Εγκατάσταση & Εκτέλεση

### Τρόπος 1: GUI App (Συνιστάται)

```powershell
# 1. Μετάβαση στον φάκελο
cd C:\Users\mimis\Desktop\stock_manager

# 2. Δημιουργία virtual environment (αν δεν έχει γίνει)
python -m venv .venv

# 3. Ενεργοποίηση virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Εγκατάσταση dependencies
pip install -r requirements.txt

# 5. Εκτέλεση GUI App
python app.py
```

### Τρόπος 2: Command Line

```powershell
# Εκτέλεση χωρίς GUI
python main.py
```

### macOS / Linux (bash/zsh)

```bash
# 1. Μετάβαση στον φάκελο
cd ~/Desktop/stock_manager

# 2. Δημιουργία virtual environment
python3 -m venv .venv

# 3. Ενεργοποίηση virtual environment
source .venv/bin/activate

# 4. Εγκατάσταση dependencies
pip install -r requirements.txt

# 5. Εκτέλεση
python main.py
```app.py                  # GUI Application (Mini App) ⭐
├── main.py                 # Command Line Version
├── requirements.txt        # Dependencies
├── README.md              # Αυτό το αρχείο
├── e56eac39-216f-413c-a208-f99c6bb26051.xlsx   # Input file (επιλέγεται από το app
```
stock_manager/
├── .venv/                  # Virtual environment (δημιουργείται αυτόματα)
├── main.py                 # Κύριος κώδικας
├── requirements.txt        # Dependencies
├── README.md              # Αυτό το αρχείο
├── e56eac39-216f-413c-a208-f99c6bb26051.xlsx   # Input file (βάλτο εδώ)
└── output.xlsx            # Output file (δημιουργείται)
```

## 📊 Λογική Συστήματος

### 1. ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ
Διαβάζει:
- **ΟΝΟΜΑ ΠΡΟΙΟΝΤΟΣ (μοναδικο)** - Primary key
- **ΚΩΔΙΚΟΣ (προαιρετικο)** - Μπορεί να είναι κενός/0
- **ΑΡΧΙΚΟ ΑΠΟΘΕΜΑ**
- **ΕΛΑΧΙΣΤΟ ΟΡΙΟ**

### 2. ΚΙΝΗΣΕΙΣ
Για κάθε κίνηση βρίσκει το προϊόν με σειρά προτεραιότητας:
1. `ΠΡΟΙΟΝ (auto)`
2. `ΠΡΟΙΟΝ (βελακι)`
3. Lookup από `ΚΩΔΙΚΟΣ (auto)`
4. Lookup από `ΚΩΔΙΚΟΣ (βελακι - προαιρετικο)`

⚠️ **Σημαντικό**: Το βασικό key είναι το **product_name** (όχι ο κωδικός)!

### 3. ΑΠΟΘΕΜΑ
Υπολογίζει ανά προϊόν:
- **ΣΥΝΟΛΟ ΕΙΣΑΓΩΓΩΝ** = Άθροισμα όλων των εισαγωγών
- **ΣΥΝΟΛΟ ΕΞΑΓΩΓΩΝ** = Άθροισμα όλων των εξαγωγών
- **ΤΡΕΧΟΝ ΑΠΟΘΕΜΑ** = ΑΡΧΙΚΟ + ΕΙΣΑΓΩΓΕΣ - ΕΞΑΓΩΓΕΣ
- **ΚΑΤΑΣΤΑΣΗ** = "ΚΑΤΩ ΑΠΟ ΟΡΙΟ" αν < ΕΛΑΧΙΣΤΟ, αλλιώς "OK"

### 4. ERRORS
Καταγράφει:
- Κινήσεις χωρίς προϊόν ή κωδικό
- Προϊόντα που δεν υπάρχουν στη ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ

## 📤 Output

Το `output.xlsx` περιέχει:
- **ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ** - Όπως το input
- **ΚΙΝΗΣΕΙΣ** - Όπως το input
- **ΑΠΟΘΕΜΑ** - Υπολογισμένοι αριθμοί (χωρίς formulas)
- **ERRORS** - Αν υπάρχουν σφάλματα

## 🛠️ Requirements

- Python 3.8+
- pandas
- openpyxl

## 💡 Tips

- Το input file πρέπει να βρίσκεται στον ίδιο φάκελο με το `main.py`
- Το output file (`output.xlsx`) δημιουργείται αυτόματα
- Αν το output file υπάρχει ήδη, θα αντικατασταθεί (overwrite)

## 📝 License

Free to use & modify
