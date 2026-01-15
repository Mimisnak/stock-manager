"""
Inventory Management System - Stock Manager
Αναπαράγει τη λογική του Excel inventory αρχείου
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import sys


def load_product_list(file_path: Path) -> pd.DataFrame:
    """
    Διαβάζει τη ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ και επιστρέφει DataFrame
    """
    print("📦 Φόρτωση ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ...")
    df = pd.read_excel(file_path, sheet_name="ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ")
    
    # Αναμενόμενες στήλες
    expected_cols = [
        "ΟΝΟΜΑ ΠΡΟΙΟΝΤΟΣ (μοναδικο)",
        "ΚΩΔΙΚΟΣ (προαιρετικο)",
        "ΑΡΧΙΚΟ ΑΠΟΘΕΜΑ",
        "ΕΛΑΧΙΣΤΟ ΟΡΙΟ"
    ]
    
    # Έλεγχος στηλών
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Λείπουν στήλες στη ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ: {missing}")
    
    print(f"✓ Φορτώθηκαν {len(df)} προϊόντα")
    return df


def load_movements(file_path: Path) -> pd.DataFrame:
    """
    Διαβάζει τις ΚΙΝΗΣΕΙΣ
    """
    print("📋 Φόρτωση ΚΙΝΗΣΕΙΣ...")
    df = pd.read_excel(file_path, sheet_name="ΚΙΝΗΣΕΙΣ")
    print(f"✓ Φορτώθηκαν {len(df)} κινήσεις")
    return df


def create_product_lookup(products_df: pd.DataFrame) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    """
    Δημιουργεί lookup structures:
    - product_dict: {product_name: {code, initial_stock, min_limit}}
    - code_to_name: {code: product_name} για lookup από κωδικό
    """
    product_dict = {}
    code_to_name = {}
    
    for _, row in products_df.iterrows():
        name = row["ΟΝΟΜΑ ΠΡΟΙΟΝΤΟΣ (μοναδικο)"]
        code = row["ΚΩΔΙΚΟΣ (προαιρετικο)"]
        
        product_dict[name] = {
            "code": code,
            "initial_stock": row["ΑΡΧΙΚΟ ΑΠΟΘΕΜΑ"],
            "min_limit": row["ΕΛΑΧΙΣΤΟ ΟΡΙΟ"]
        }
        
        # Αν υπάρχει κωδικός (όχι NaN, None, 0, "")
        if pd.notna(code) and code != 0 and str(code).strip() != "":
            code_to_name[str(code)] = name
    
    return product_dict, code_to_name


def resolve_product_name(row: pd.Series, code_to_name: Dict[str, str]) -> Optional[str]:
    """
    Βρίσκει το product_name από μια κίνηση.
    Σειρά προτεραιότητας:
    1. ΠΡΟΙΟΝ (auto)
    2. ΠΡΟΙΟΝ (βελακι)
    3. Lookup από ΚΩΔΙΚΟΣ (auto)
    4. Lookup από ΚΩΔΙΚΟΣ (βελακι - προαιρετικο)
    
    Returns: product_name ή None αν δεν βρέθηκε
    """
    # 1. ΠΡΟΙΟΝ (auto)
    if "ΠΡΟΙΟΝ (auto)" in row and pd.notna(row["ΠΡΟΙΟΝ (auto)"]) and str(row["ΠΡΟΙΟΝ (auto)"]).strip():
        return str(row["ΠΡΟΙΟΝ (auto)"])
    
    # 2. ΠΡΟΙΟΝ (βελακι)
    if "ΠΡΟΙΟΝ (βελακι)" in row and pd.notna(row["ΠΡΟΙΟΝ (βελακι)"]) and str(row["ΠΡΟΙΟΝ (βελακι)"]).strip():
        return str(row["ΠΡΟΙΟΝ (βελακι)"])
    
    # 3. ΚΩΔΙΚΟΣ (auto)
    if "ΚΩΔΙΚΟΣ (auto)" in row and pd.notna(row["ΚΩΔΙΚΟΣ (auto)"]):
        code = str(row["ΚΩΔΙΚΟΣ (auto)"])
        if code in code_to_name:
            return code_to_name[code]
    
    # 4. ΚΩΔΙΚΟΣ (βελακι - προαιρετικο)
    if "ΚΩΔΙΚΟΣ (βελακι - προαιρετικο)" in row and pd.notna(row["ΚΩΔΙΚΟΣ (βελακι - προαιρετικο)"]):
        code = str(row["ΚΩΔΙΚΟΣ (βελακι - προαιρετικο)"])
        if code in code_to_name:
            return code_to_name[code]
    
    return None


def process_movements(
    movements_df: pd.DataFrame,
    product_dict: Dict[str, Dict[str, Any]],
    code_to_name: Dict[str, str]
) -> Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Επεξεργάζεται τις κινήσεις και υπολογίζει τα αθροίσματα ανά προϊόν.
    
    Returns:
    - aggregated: {product_name: {total_in, total_out}}
    - errors: λίστα με κινήσεις που έχουν σφάλματα
    """
    print("⚙️  Επεξεργασία κινήσεων...")
    
    aggregated = {name: {"total_in": 0.0, "total_out": 0.0} for name in product_dict.keys()}
    errors = []
    
    for row_num, (_, row) in enumerate(movements_df.iterrows(), start=1):
        product_name = resolve_product_name(row, code_to_name)
        
        # Validation
        if product_name is None:
            errors.append({
                "row_index": row_num + 1,  # +1 για το header row
                "error": "Δεν βρέθηκε προϊόν ή κωδικός",
                "data": row.to_dict()
            })
            continue
        
        if product_name not in product_dict:
            errors.append({
                "row_index": row_num + 1,
                "error": f"Το προϊόν '{product_name}' δεν υπάρχει στη ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ",
                "data": row.to_dict()
            })
            continue
        
        # Άθροισμα εισαγωγών/εξαγωγών
        inbound = row.get("ΕΙΣΑΓΩΓΗ", 0)
        outbound = row.get("ΕΞΑΓΩΓΗ", 0)
        
        if pd.notna(inbound):
            aggregated[product_name]["total_in"] += float(inbound)
        
        if pd.notna(outbound):
            aggregated[product_name]["total_out"] += float(outbound)
    
    print(f"✓ Επεξεργάστηκαν {len(movements_df)} κινήσεις")
    if errors:
        print(f"⚠️  Βρέθηκαν {len(errors)} σφάλματα")
    
    return aggregated, errors


def calculate_stock(
    product_dict: Dict[str, Dict[str, Any]],
    aggregated: Dict[str, Dict[str, Any]]
) -> pd.DataFrame:
    """
    Υπολογίζει το τρέχον απόθεμα και τη κατάσταση για κάθε προϊόν
    """
    print("📊 Υπολογισμός αποθέματος...")
    
    results = []
    
    for product_name, info in product_dict.items():
        initial = info["initial_stock"]
        min_limit = info["min_limit"]
        total_in = aggregated[product_name]["total_in"]
        total_out = aggregated[product_name]["total_out"]
        
        current_stock = initial + total_in - total_out
        status = "ΚΑΤΩ ΑΠΟ ΟΡΙΟ" if current_stock < min_limit else "OK"
        
        results.append({
            "ΠΡΟΙΟΝ": product_name,
            "ΚΩΔΙΚΟΣ (προαιρετικο)": info["code"],
            "ΑΡΧΙΚΟ": initial,
            "ΣΥΝΟΛΟ ΕΙΣΑΓΩΓΩΝ": total_in,
            "ΣΥΝΟΛΟ ΕΞΑΓΩΓΩΝ": total_out,
            "ΤΡΕΧΟΝ ΑΠΟΘΕΜΑ": current_stock,
            "ΕΛΑΧΙΣΤΟ": min_limit,
            "ΚΑΤΑΣΤΑΣΗ": status
        })
    
    df = pd.DataFrame(results)
    
    low_stock_count = len(df[df["ΚΑΤΑΣΤΑΣΗ"] == "ΚΑΤΩ ΑΠΟ ΟΡΙΟ"])
    if low_stock_count > 0:
        print(f"⚠️  {low_stock_count} προϊόντα κάτω από το όριο!")
    else:
        print(f"✓ Όλα τα προϊόντα εντός ορίων")
    
    return df


def create_errors_dataframe(errors: List[Dict[str, Any]]) -> Optional[pd.DataFrame]:
    """
    Δημιουργεί DataFrame για τα errors (αν υπάρχουν)
    """
    if not errors:
        return None
    
    # Flatten τα data dictionaries
    flattened = []
    for err in errors:
        flat = {
            "ROW_INDEX": err["row_index"],
            "ERROR": err["error"]
        }
        flat.update(err["data"])
        flattened.append(flat)
    
    return pd.DataFrame(flattened)


def write_output(
    output_path: Path,
    products_df: pd.DataFrame,
    movements_df: pd.DataFrame,
    stock_df: pd.DataFrame,
    errors_df: Optional[pd.DataFrame]
):
    """
    Γράφει το output.xlsx με όλα τα sheets
    """
    print(f"💾 Αποθήκευση στο {output_path}...")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        products_df.to_excel(writer, sheet_name="ΛΙΣΤΑ_ΠΡΟΙΟΝΤΩΝ", index=False)
        movements_df.to_excel(writer, sheet_name="ΚΙΝΗΣΕΙΣ", index=False)
        stock_df.to_excel(writer, sheet_name="ΑΠΟΘΕΜΑ", index=False)
        
        if errors_df is not None:
            errors_df.to_excel(writer, sheet_name="ERRORS", index=False)
    
    print(f"✅ Ολοκληρώθηκε! Αρχείο: {output_path}")


def main():
    """
    Main function
    """
    print("=" * 60)
    print("🏪 STOCK MANAGER - Inventory System")
    print("=" * 60)
    
    # Paths
    input_file = Path("e56eac39-216f-413c-a208-f99c6bb26051.xlsx")
    output_file = Path("output.xlsx")
    
    # Έλεγχος ύπαρξης input file
    if not input_file.exists():
        print(f"❌ Σφάλμα: Το αρχείο '{input_file}' δεν βρέθηκε!")
        print(f"   Βεβαιώσου ότι βρίσκεται στον ίδιο φάκελο με το main.py")
        sys.exit(1)
    
    try:
        # 1. Φόρτωση δεδομένων
        products_df = load_product_list(input_file)
        movements_df = load_movements(input_file)
        
        # 2. Δημιουργία lookup structures
        product_dict, code_to_name = create_product_lookup(products_df)
        
        # 3. Επεξεργασία κινήσεων
        aggregated, errors = process_movements(movements_df, product_dict, code_to_name)
        
        # 4. Υπολογισμός αποθέματος
        stock_df = calculate_stock(product_dict, aggregated)
        
        # 5. Δημιουργία errors DataFrame (αν υπάρχουν)
        errors_df = create_errors_dataframe(errors)
        
        # 6. Εγγραφή output
        write_output(output_file, products_df, movements_df, stock_df, errors_df)
        
        print("\n" + "=" * 60)
        print("✨ Επιτυχής ολοκλήρωση!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Σφάλμα: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
