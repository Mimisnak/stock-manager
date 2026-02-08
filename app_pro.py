"""
Stock Manager PRO - Επαγγελματική Εφαρμογή Διαχείρισης Αποθήκης
Modern UI με Dashboard, Στατιστικά & Γραφήματα
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json
from collections import Counter
from typing import Any


class ModernButton(tk.Button):
    """Modern styled button"""
    def __init__(self, parent: tk.Widget, **kwargs: Any) -> None:
        super().__init__(
            parent,
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            borderwidth=0,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.default_bg = kwargs.get('bg', '#3498db')
    
    def on_enter(self, e):
        self['background'] = self.lighten_color(self.default_bg)
    
    def on_leave(self, e):
        self['background'] = self.default_bg
    
    def lighten_color(self, color):
        # Simple color lightening
        colors = {
            '#27ae60': '#2ecc71',
            '#3498db': '#5dade2',
            '#e74c3c': '#ec7063',
            '#e67e22': '#f39c12',
            '#9b59b6': '#bb8fce',
            '#16a085': '#1abc9c'
        }
        return colors.get(color, '#5dade2')


class StockManagerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🏪 Stock Manager PRO - Διαχείριση Αποθήκης")
        self.root.geometry("1600x900")
        self.root.resizable(True, True)
        
        # Modern colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'purple': '#9b59b6',
            'teal': '#16a085'
        }
        
        # Data files
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.products_file = self.data_dir / "products.json"
        self.movements_file = self.data_dir / "movements.json"
        self.categories_file = self.data_dir / "categories.json"
        
        # Backup directory
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load data
        self.categories = self.load_categories()
        self.products = self.load_products()
        self.movements = self.load_movements()
        
        # Auto backup on start
        self.auto_backup()
        
        # Search vars
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        
        self.setup_ui()
        self.refresh_all()
        
        # Αυτόματη ενημέρωση dashboard κάθε 30 δευτερόλεπτα
        self.auto_refresh_dashboard()
        
        # Handler για ασφαλές κλείσιμο
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup Modern UI"""
        # Top bar
        top_bar = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo & Title
        title_frame = tk.Frame(top_bar, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            title_frame,
            text="🏪",
            bg=self.colors['primary'],
            fg="white",
            font=("Segoe UI", 28)
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_frame,
            text="STOCK MANAGER PRO",
            bg=self.colors['primary'],
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(side=tk.LEFT, padx=10)
        
        # Quick stats in top bar
        stats_frame = tk.Frame(top_bar, bg=self.colors['primary'])
        stats_frame.pack(side=tk.RIGHT, padx=20)
        
        self.stat_products = self.create_stat_widget(stats_frame, "📦", "0", "Προϊόντα")
        self.stat_products.pack(side=tk.LEFT, padx=10)
        
        self.stat_low = self.create_stat_widget(stats_frame, "⚠️", "0", "Χαμηλά")
        self.stat_low.pack(side=tk.LEFT, padx=10)
        
        self.stat_movements = self.create_stat_widget(stats_frame, "📋", "0", "Κινήσεις")
        self.stat_movements.pack(side=tk.LEFT, padx=10)
        
        # Main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_products_tab()
        self.create_movements_tab()
        self.create_history_tab()
        self.create_stock_tab()
        self.create_reports_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="✓ Έτοιμο",
            font=("Segoe UI", 9),
            bg=self.colors['light'],
            fg=self.colors['dark'],
            anchor=tk.W,
            padx=15,
            pady=8
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Apply modern style
        self.apply_style()
    
    def create_stat_widget(self, parent, icon, value, label):
        """Create a stat display widget"""
        frame = tk.Frame(parent, bg=self.colors['secondary'], padx=15, pady=8)
        
        tk.Label(
            frame,
            text=icon,
            bg=self.colors['secondary'],
            fg="white",
            font=("Segoe UI", 16)
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        text_frame = tk.Frame(frame, bg=self.colors['secondary'])
        text_frame.pack(side=tk.LEFT)
        
        value_label = tk.Label(
            text_frame,
            text=value,
            bg=self.colors['secondary'],
            fg="white",
            font=("Segoe UI", 14, "bold")
        )
        value_label.pack(anchor=tk.W)
        
        tk.Label(
            text_frame,
            text=label,
            bg=self.colors['secondary'],
            fg="#bdc3c7",
            font=("Segoe UI", 8)
        ).pack(anchor=tk.W)
        
        frame.value_label = value_label  # type: ignore
        return frame
    
    def create_dashboard_tab(self):
        """Tab: Dashboard με στατιστικά"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📊 DASHBOARD")
        
        # Header
        header = tk.Frame(tab, bg=self.colors['info'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 Επισκόπηση Αποθήκης",
            bg=self.colors['info'],
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Content
        content = tk.Frame(tab, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Stats cards
        cards_frame = tk.Frame(content, bg="white")
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.card_total = self.create_stat_card(
            cards_frame, "📦 Συνολικά Προϊόντα", "0", self.colors['info']
        )
        self.card_total.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.card_stock_value = self.create_stat_card(
            cards_frame, "� Συνολική Ποσότητα", "0", self.colors['success']
        )
        self.card_stock_value.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.card_low_stock = self.create_stat_card(
            cards_frame, "⚠️ Χαμηλό Απόθεμα", "0", self.colors['warning']
        )
        self.card_low_stock.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.card_movements_today = self.create_stat_card(
            cards_frame, "📋 Κινήσεις Σήμερα", "0", self.colors['purple']
        )
        self.card_movements_today.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Recent activity
        activity_frame = tk.LabelFrame(
            content,
            text="📌 Πρόσφατες Κινήσεις",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg=self.colors['dark']
        )
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.activity_tree = self.create_simple_table(
            activity_frame,
            ["Ημερομηνία", "Προϊόν", "Τύπος", "Ποσότητα"]
        )
    
    def create_stat_card(self, parent, title, value, color):
        """Create a dashboard stat card"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.pack_propagate(False)
        card.configure(height=120)
        
        tk.Label(
            card,
            text=title,
            bg=color,
            fg="white",
            font=("Segoe UI", 11)
        ).pack(pady=(15, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            bg=color,
            fg="white",
            font=("Segoe UI", 28, "bold")
        )
        value_label.pack()
        
        card.value_label = value_label  # type: ignore
        return card
    
    def create_products_tab(self):
        """Tab: Προϊόντα με search"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📦 ΠΡΟΙΟΝΤΑ")
        
        # Toolbar
        toolbar = tk.Frame(tab, bg=self.colors['light'], height=70)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # Buttons
        btn_frame = tk.Frame(toolbar, bg=self.colors['light'])
        btn_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        ModernButton(
            btn_frame,
            text="➕ Νέο",
            command=self.add_product,
            bg=self.colors['success'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="✏️ Επεξεργασία",
            command=self.edit_product,
            bg=self.colors['info'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="🗑️ Διαγραφή",
            command=self.delete_product,
            bg=self.colors['danger'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="🏷️ Κατηγορίες",
            command=self.manage_categories,
            bg=self.colors['purple'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Search
        search_frame = tk.Frame(toolbar, bg=self.colors['light'])
        search_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            search_frame,
            text="🔍",
            bg=self.colors['light'],
            font=("Segoe UI", 14)
        ).pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            width=30,
            relief=tk.FLAT,
            borderwidth=2
        )
        search_entry.pack(side=tk.LEFT, padx=5, ipady=6)
        # Αυτόματη ενημέρωση καθώς πληκτρολογείς
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_products())
        
        # Category Filter
        tk.Label(
            search_frame,
            text="Κατηγορία:",
            bg=self.colors['light'],
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.category_filter = ttk.Combobox(
            search_frame,
            font=("Segoe UI", 10),
            width=18,
            state="readonly"
        )
        self.category_filter['values'] = ["Όλες"] + self.categories
        self.category_filter.current(0)
        self.category_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_products())
        self.category_filter.pack(side=tk.LEFT, padx=5)
        
        # Table
        self.products_tree = self.create_modern_table(
            tab,
            ["#", "Προϊόν", "Κατηγορία", "Κωδικός", "Αρχικό", "Ελάχιστο", "Τρέχον Απόθεμα", "Κατάσταση"]
        )
    
    def create_movements_tab(self):
        """Tab: Κινήσεις"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📋 ΚΙΝΗΣΕΙΣ")
        
        # Toolbar
        toolbar = tk.Frame(tab, bg=self.colors['light'], height=70)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        btn_frame = tk.Frame(toolbar, bg=self.colors['light'])
        btn_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        ModernButton(
            btn_frame,
            text="📥 Εισαγωγή",
            command=lambda: self.add_movement("in"),
            bg=self.colors['success'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="📤 Εξαγωγή",
            command=lambda: self.add_movement("out"),
            bg=self.colors['warning'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="🗑️ Διαγραφή",
            command=self.delete_movement,
            bg=self.colors['danger'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Filter
        filter_frame = tk.Frame(toolbar, bg=self.colors['light'])
        filter_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            filter_frame,
            text="Φίλτρο:",
            bg=self.colors['light'],
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.movement_filter = ttk.Combobox(
            filter_frame,
            font=("Segoe UI", 10),
            width=15,
            state="readonly"
        )
        self.movement_filter['values'] = ["Όλες", "Εισαγωγές", "Εξαγωγές", "Σήμερα", "Τελευταία 7 ημέρες"]
        self.movement_filter.current(0)
        self.movement_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_movements())
        self.movement_filter.pack(side=tk.LEFT, padx=5)
        
        # Table
        self.movements_tree = self.create_modern_table(
            tab,
            ["ID", "Ημερομηνία", "Προϊόν", "Τύπος", "Ποσότητα", "Σημειώσεις"]
        )
    
    def create_history_tab(self):
        """Tab: Ημερολόγιο/Ιστορικό Κινήσεων με δυνατότητα εξαγωγής"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📅 ΗΜΕΡΟΛΟΓΙΟ")
        
        # Toolbar
        toolbar = tk.Frame(tab, bg=self.colors['light'], height=90)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # Left section - Date filters
        filter_frame = tk.Frame(toolbar, bg=self.colors['light'])
        filter_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            filter_frame,
            text="📅 Φίλτρα Ημερομηνιών:",
            bg=self.colors['light'],
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        
        # From date
        tk.Label(
            filter_frame,
            text="Από:",
            bg=self.colors['light'],
            font=("Segoe UI", 10)
        ).grid(row=1, column=0, padx=5)
        
        self.history_from_date = tk.Entry(
            filter_frame,
            font=("Segoe UI", 10),
            width=12
        )
        self.history_from_date.grid(row=1, column=1, padx=5)
        self.history_from_date.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        # To date
        tk.Label(
            filter_frame,
            text="Έως:",
            bg=self.colors['light'],
            font=("Segoe UI", 10)
        ).grid(row=1, column=2, padx=5)
        
        self.history_to_date = tk.Entry(
            filter_frame,
            font=("Segoe UI", 10),
            width=12
        )
        self.history_to_date.grid(row=1, column=3, padx=5)
        self.history_to_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Quick filters
        quick_frame = tk.Frame(filter_frame, bg=self.colors['light'])
        quick_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        def set_today():
            today = datetime.now().strftime("%Y-%m-%d")
            self.history_from_date.delete(0, tk.END)
            self.history_from_date.insert(0, today)
            self.history_to_date.delete(0, tk.END)
            self.history_to_date.insert(0, today)
            self.refresh_history()
        
        def set_week():
            today = datetime.now()
            week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
            self.history_from_date.delete(0, tk.END)
            self.history_from_date.insert(0, week_ago)
            self.history_to_date.delete(0, tk.END)
            self.history_to_date.insert(0, today.strftime("%Y-%m-%d"))
            self.refresh_history()
        
        def set_month():
            today = datetime.now()
            month_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            self.history_from_date.delete(0, tk.END)
            self.history_from_date.insert(0, month_ago)
            self.history_to_date.delete(0, tk.END)
            self.history_to_date.insert(0, today.strftime("%Y-%m-%d"))
            self.refresh_history()
        
        ModernButton(
            quick_frame,
            text="Σήμερα",
            command=set_today,
            bg=self.colors['info'],
            fg="white",
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=2)
        
        ModernButton(
            quick_frame,
            text="7 Ημέρες",
            command=set_week,
            bg=self.colors['info'],
            fg="white",
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=2)
        
        ModernButton(
            quick_frame,
            text="30 Ημέρες",
            command=set_month,
            bg=self.colors['info'],
            fg="white",
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=2)
        
        ModernButton(
            quick_frame,
            text="🔄 Ανανέωση",
            command=self.refresh_history,
            bg=self.colors['success'],
            fg="white",
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=2)
        
        # Right section - Export buttons
        export_frame = tk.Frame(toolbar, bg=self.colors['light'])
        export_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            export_frame,
            text="📤 Εξαγωγή:",
            bg=self.colors['light'],
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        btn_container = tk.Frame(export_frame, bg=self.colors['light'])
        btn_container.pack()
        
        ModernButton(
            btn_container,
            text="📊 Excel",
            command=self.export_history_to_excel,
            bg=self.colors['success'],
            fg="white",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_container,
            text="📄 PDF",
            command=self.export_history_to_pdf,
            bg=self.colors['danger'],
            fg="white",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Summary frame
        summary_frame = tk.Frame(tab, bg=self.colors['light'], height=60)
        summary_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        summary_frame.pack_propagate(False)
        
        self.history_summary_label = tk.Label(
            summary_frame,
            text="",
            bg=self.colors['light'],
            fg=self.colors['dark'],
            font=("Segoe UI", 10)
        )
        self.history_summary_label.pack(pady=15)
        
        # Table
        self.history_tree = self.create_modern_table(
            tab,
            ["ID", "Ημερομηνία", "Ώρα", "Προϊόν", "Κατηγορία", "Τύπος", "Ποσότητα", "Σημειώσεις"]
        )
    
    def create_stock_tab(self):
        """Tab: Απόθεμα"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📊 ΑΠΟΘΕΜΑ")
        
        # Toolbar
        toolbar = tk.Frame(tab, bg=self.colors['light'], height=70)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        btn_frame = tk.Frame(toolbar, bg=self.colors['light'])
        btn_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        ModernButton(
            btn_frame,
            text="🔄 Ανανέωση",
            command=self.refresh_stock,
            bg=self.colors['info'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="💾 Εξαγωγή Excel",
            command=self.export_to_excel,
            bg=self.colors['success'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="📊 Αναφορά PDF",
            command=self.export_to_pdf,
            bg=self.colors['purple'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Filter
        filter_frame = tk.Frame(toolbar, bg=self.colors['light'])
        filter_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            filter_frame,
            text="Εμφάνιση:",
            bg=self.colors['light'],
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.stock_filter = ttk.Combobox(
            filter_frame,
            font=("Segoe UI", 10),
            width=18,
            state="readonly"
        )
        self.stock_filter['values'] = ["Όλα", "Μόνο Χαμηλά", "Μόνο OK"]
        self.stock_filter.current(0)
        self.stock_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_stock())
        self.stock_filter.pack(side=tk.LEFT, padx=5)
        
        # Table
        self.stock_tree = self.create_modern_table(
            tab,
            ["Προϊόν", "Κωδικός", "Αρχικό", "Εισαγωγές", "Εξαγωγές", "Τρέχον", "Ελάχιστο", "Κατάσταση"]
        )
    
    def create_reports_tab(self):
        """Tab: Αναφορές"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📊 ΑΝΑΦΟΡΕΣ")
        
        # Toolbar
        toolbar = tk.Frame(tab, bg=self.colors['light'], height=70)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        btn_frame = tk.Frame(toolbar, bg=self.colors['light'])
        btn_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        ModernButton(
            btn_frame,
            text="🔄 Ανανέωση",
            command=self.refresh_reports,
            bg=self.colors['info'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="💾 Backup",
            command=self.manual_backup,
            bg=self.colors['success'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="📥 Restore",
            command=self.restore_backup,
            bg=self.colors['warning'],
            fg="white",
            padx=25,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Content with scrollbar
        content_frame = tk.Frame(tab, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Statistics Cards
        stats_frame = tk.Frame(scrollable_frame, bg="white")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.report_total_products = self.create_report_card(stats_frame, "📦 Συνολικά Προϊόντα", "0", self.colors['info'])
        self.report_total_products.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.report_total_movements = self.create_report_card(stats_frame, "📋 Συνολικές Κινήσεις", "0", self.colors['purple'])
        self.report_total_movements.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.report_stock_value = self.create_report_card(stats_frame, "💰 Αξία Αποθέματος", "0", self.colors['success'])
        self.report_stock_value.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Most Active Products
        active_frame = tk.LabelFrame(
            scrollable_frame,
            text="🔥 Πιο Ενεργά Προϊόντα (Top 5)",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg=self.colors['dark']
        )
        active_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.most_active_tree = self.create_simple_table(
            active_frame,
            ["Προϊόν", "Συνολικές Κινήσεις", "Εισαγωγές", "Εξαγωγές"]
        )
        
        # Least Active Products
        least_frame = tk.LabelFrame(
            scrollable_frame,
            text="💤 Λιγότερο Ενεργά Προϊόντα (Top 5)",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg=self.colors['dark']
        )
        least_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.least_active_tree = self.create_simple_table(
            least_frame,
            ["Προϊόν", "Συνολικές Κινήσεις", "Εισαγωγές", "Εξαγωγές"]
        )
        
        # Monthly Summary
        monthly_frame = tk.LabelFrame(
            scrollable_frame,
            text="📅 Μηνιαίο Σύνολο",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg=self.colors['dark']
        )
        monthly_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.monthly_tree = self.create_simple_table(
            monthly_frame,
            ["Μήνας", "Εισαγωγές", "Εξαγωγές", "Σύνολο Κινήσεων"]
        )
    
    def create_report_card(self, parent, title, value, color):
        """Create a report stat card"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.pack_propagate(False)
        card.configure(height=100)
        
        tk.Label(
            card,
            text=title,
            bg=color,
            fg="white",
            font=("Segoe UI", 10)
        ).pack(pady=(10, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            bg=color,
            fg="white",
            font=("Segoe UI", 24, "bold")
        )
        value_label.pack()
        
        card.value_label = value_label  # type: ignore
        return card
    
    def create_modern_table(self, parent, columns):
        """Create modern styled table with sortable columns"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical")
        hsb = ttk.Scrollbar(frame, orient="horizontal")
        
        # Treeview
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="browse"
        )
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Configure columns with sorting
        for col in columns:
            tree.heading(col, text=col, anchor=tk.W)
            tree.column(col, width=120, anchor=tk.W)
            # Add click event for sorting
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, c, False))
        
        # Grid
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Tags
        tree.tag_configure("low", background="#ffebee", foreground="#c62828")
        tree.tag_configure("ok", background="#e8f5e9", foreground="#2e7d32")
        tree.tag_configure("evenrow", background="#f5f5f5")
        tree.tag_configure("oddrow", background="white")
        
        return tree
    
    def sort_treeview(self, tree, col, reverse):
        """Sort treeview by column"""
        try:
            # Get all rows
            data_list = [(tree.set(child, col), child) for child in tree.get_children('')]
            
            # Try to sort numerically first, if fails sort alphabetically
            try:
                # Try numeric sort
                data_list.sort(key=lambda t: float(t[0].replace('📥 ', '').replace('📤 ', '').replace('€', '').replace(',', '').strip()), reverse=reverse)
            except:
                # Fallback to string sort
                data_list.sort(key=lambda t: t[0].lower(), reverse=reverse)
            
            # Rearrange items
            for index, (val, child) in enumerate(data_list):
                tree.move(child, '', index)
                # Update row colors
                if index % 2 == 0:
                    tree.item(child, tags=('evenrow',))
                else:
                    tree.item(child, tags=('oddrow',))
            
            # Update heading to show sort direction
            for c in tree['columns']:
                current_text = tree.heading(c)['text']
                # Remove existing arrows
                clean_text = current_text.replace(' ▲', '').replace(' ▼', '')
                if c == col:
                    # Add arrow to sorted column
                    tree.heading(c, text=clean_text + (' ▼' if reverse else ' ▲'))
                    # Set command to reverse sort next time
                    tree.heading(c, command=lambda c=c: self.sort_treeview(tree, c, not reverse))
                else:
                    tree.heading(c, text=clean_text)
                    tree.heading(c, command=lambda c=c: self.sort_treeview(tree, c, False))
        except Exception as e:
            print(f"Sort error: {e}")
    
    def create_simple_table(self, parent, columns):
        """Simple table for dashboard"""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(frame, orient="vertical")
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            height=8
        )
        
        vsb.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        return tree
    
    def apply_style(self):
        """Apply modern ttk style"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook style
        style.configure(
            'TNotebook',
            background='white',
            borderwidth=0
        )
        style.configure(
            'TNotebook.Tab',
            background=self.colors['light'],
            foreground=self.colors['dark'],
            padding=[20, 10],
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', 'white')],
            foreground=[('selected', self.colors['info'])]
        )
        
        # Treeview style
        style.configure(
            'Treeview',
            background="white",
            foreground=self.colors['dark'],
            fieldbackground="white",
            borderwidth=0,
            font=("Segoe UI", 10),
            rowheight=30
        )
        style.configure(
            'Treeview.Heading',
            background=self.colors['info'],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map(
            'Treeview',
            background=[('selected', self.colors['info'])],
            foreground=[('selected', 'white')]
        )
    
    # Data Management (same as before)
    
    def load_categories(self):
        """Load categories from file or use defaults"""
        if self.categories_file.exists():
            with open(self.categories_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Default categories
        return [
            "🍕 Τρόφιμα",
            "🍺 Ποτά", 
            "🧴 Καθαριστικά",
            "📦 Υλικά Συσκευασίας",
            "🔧 Εργαλεία",
            "📄 Γραφική Ύλη",
            "💊 Φαρμακευτικά",
            "🎨 Καλλυντικά",
            "🏠 Οικιακά Είδη",
            "⚡ Άλλο"
        ]
    
    def save_categories(self):
        """Save categories to file"""
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(self.categories, f, ensure_ascii=False, indent=2)
        self.auto_backup()
    
    def load_products(self):
        if self.products_file.exists():
            with open(self.products_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_products(self):
        with open(self.products_file, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        self.auto_backup()
    
    def load_movements(self):
        if self.movements_file.exists():
            with open(self.movements_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_movements(self):
        with open(self.movements_file, 'w', encoding='utf-8') as f:
            json.dump(self.movements, f, ensure_ascii=False, indent=2)
        self.auto_backup()
    
    def auto_backup(self):
        """Automatically backup data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"backup_{timestamp}.json"
            
            backup_data = {
                'timestamp': timestamp,
                'products': self.products,
                'movements': self.movements,
                'categories': self.categories
            }
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            # Keep only last 20 backups
            backups = sorted(self.backup_dir.glob("backup_*.json"))
            if len(backups) > 20:
                for old_backup in backups[:-20]:
                    old_backup.unlink()
        except Exception as e:
            print(f"Backup error: {e}")
    
    def manual_backup(self):
        """Manual backup with notification"""
        try:
            self.auto_backup()
            
            # Εμφάνιση λεπτομερειών
            backup_dir = self.backup_dir
            backups = sorted(backup_dir.glob("backup_*.json"), reverse=True)
            
            if backups:
                latest = backups[0]
                timestamp_str = latest.stem.replace("backup_", "")
                dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                messagebox.showinfo(
                    "✅ Backup Επιτυχές",
                    f"Το backup ολοκληρώθηκε επιτυχώς!\n\n"
                    f"📁 Αρχείο: {latest.name}\n"
                    f"📅 Ημερομηνία: {dt.strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"💾 Μέγεθος: {latest.stat().st_size / 1024:.1f} KB\n\n"
                    f"📦 Συνολικά backups: {len(backups)}"
                )
            
            self.show_notification("✓ Backup ολοκληρώθηκε", "success")
        except Exception as e:
            self.show_notification(f"✗ Σφάλμα backup: {e}", "error")
            messagebox.showerror("Σφάλμα", f"Πρόβλημα κατά το backup:\n{e}")
    
    def restore_backup(self):
        """Restore from backup"""
        try:
            backups = sorted(self.backup_dir.glob("backup_*.json"), reverse=True)
            if not backups:
                messagebox.showwarning(
                    "Δεν υπάρχουν Backups",
                    "Δεν βρέθηκαν διαθέσιμα backups!\n\n"
                    "Τα backups δημιουργούνται αυτόματα κάθε φορά\n"
                    "που κάνετε αλλαγές στα δεδομένα."
                )
                self.show_notification("⚠ Δεν υπάρχουν backups", "warning")
                return
            
            dialog = BackupRestoreDialog(self.root, backups)
            if dialog.result:
                try:
                    # Διάβασμα backup
                    with open(dialog.result, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                    
                    # Ενημέρωση δεδομένων
                    self.products = backup_data.get('products', [])
                    self.movements = backup_data.get('movements', [])
                    self.categories = backup_data.get('categories', self.categories)
                    
                    # Αποθήκευση των δεδομένων
                    self.save_products()
                    self.save_movements()
                    self.save_categories()
                    
                    # Ενημέρωση του category filter
                    self.category_filter['values'] = ["Όλες"] + self.categories
                    self.category_filter.set("Όλες")
                    
                    # Καθαρισμός του search field
                    self.search_var.set("")
                    
                    # Ανανέωση UI - Διαγραφή όλων των items από τα treeviews
                    for tree in [self.products_tree, self.movements_tree, 
                                self.stock_tree, self.most_active_tree]:
                        for item in tree.get_children():
                            tree.delete(item)
                    
                    # Πλήρης ανανέωση όλων των tabs
                    self.refresh_all()
                    self.update_statistics()
                    self.apply_filters()
                    
                    # Επαναφορά στο πρώτο tab
                    self.notebook.select(0)
                    
                    messagebox.showinfo(
                        "✅ Επαναφορά Επιτυχής",
                        f"Τα δεδομένα επαναφέρθηκαν επιτυχώς!\n\n"
                        f"📦 Προϊόντα: {len(self.products)}\n"
                        f"📋 Κινήσεις: {len(self.movements)}\n"
                        f"🏷️ Κατηγορίες: {len(self.categories)}"
                    )
                    
                    self.show_notification("✓ Επαναφορά ολοκληρώθηκε", "success")
                except Exception as e:
                    self.show_notification(f"✗ Σφάλμα: {e}", "error")
                    messagebox.showerror("Σφάλμα", f"Πρόβλημα επαναφοράς:\n{e}")
        except Exception as e:
            self.show_notification(f"✗ Σφάλμα: {e}", "error")
            messagebox.showerror("Σφάλμα", f"Πρόβλημα:\n{e}")
    
    def get_current_stock(self, product_id):
        """Get current stock for a product"""
        product = next((p for p in self.products if p['id'] == product_id), None)
        if not product:
            return 0
        
        total_in = sum(m['quantity'] for m in self.movements 
                      if m['product_id'] == product_id and m['type'] == 'in')
        total_out = sum(m['quantity'] for m in self.movements 
                       if m['product_id'] == product_id and m['type'] == 'out')
        
        return product['initial_stock'] + total_in - total_out
    
    # Product Operations (same as before but with notifications)
    
    def add_product(self):
        dialog = ProductDialog(self.root, "Νέο Προϊόν", categories=self.categories)
        if dialog.result:
            max_id = max([p['id'] for p in self.products], default=0)
            dialog.result['id'] = max_id + 1
            self.products.append(dialog.result)
            self.save_products()
            self.refresh_all()
            # Ενημέρωση όλων των tabs άμεσα
            self.root.update_idletasks()
            self.show_notification(f"✓ Προστέθηκε: {dialog.result['name']}", "success")
    
    def edit_product(self):
        selected = self.products_tree.selection()
        if not selected:
            self.show_notification("⚠ Επιλέξτε προϊόν", "warning")
            return
        
        # Λήψη του πραγματικού ID από το iid
        product_id = int(selected[0])
        product = next((p for p in self.products if p['id'] == product_id), None)
        
        if product:
            dialog = ProductDialog(self.root, "Επεξεργασία", product=product, categories=self.categories)
            if dialog.result:
                for key, value in dialog.result.items():  # type: ignore
                    product[key] = value
                self.save_products()
                self.refresh_all()
                # Ενημέρωση όλων των tabs άμεσα
                self.root.update_idletasks()
                self.show_notification(f"✓ Ενημερώθηκε: {product['name']}", "success")
    
    def manage_categories(self):
        """Open category management dialog"""
        dialog = CategoryDialog(self.root, self.categories)
        if dialog.result:
            self.categories = dialog.result
            self.save_categories()
            self.category_filter['values'] = ["Όλες"] + self.categories
            self.refresh_all()
            self.show_notification("✓ Κατηγορίες ενημερώθηκαν", "success")
    
    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            self.show_notification("⚠ Επιλέξτε προϊόν", "warning")
            return
        
        item = self.products_tree.item(selected[0])
        # Λήψη του πραγματικού ID από το iid
        product_id = int(selected[0])
        product_name = item['values'][1]
        
        if messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή '{product_name}';"):
            self.products = [p for p in self.products if p['id'] != product_id]
            self.movements = [m for m in self.movements if m['product_id'] != product_id]
            self.save_products()
            self.save_movements()
            self.refresh_all()
            # Ενημέρωση όλων των tabs άμεσα
            self.root.update_idletasks()
            self.show_notification(f"✓ Διαγράφηκε: {product_name}", "success")
    
    def add_movement(self, movement_type):
        if not self.products:
            self.show_notification("⚠ Προσθέστε πρώτα προϊόντα", "warning")
            return
        
        dialog = MovementDialog(self.root, movement_type, self.products)
        if dialog.result:
            max_id = max([m['id'] for m in self.movements], default=0)
            dialog.result['id'] = max_id + 1
            dialog.result['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.movements.append(dialog.result)
            self.save_movements()
            self.refresh_all()
            # Ενημέρωση όλων των tabs άμεσα
            self.root.update_idletasks()
            
            product_name = next((p['name'] for p in self.products if p['id'] == dialog.result['product_id']), "")
            icon = "📥" if movement_type == "in" else "📤"
            self.show_notification(f"{icon} Καταχωρήθηκε: {product_name}", "success")
    
    def delete_movement(self):
        selected = self.movements_tree.selection()
        if not selected:
            self.show_notification("⚠ Επιλέξτε κίνηση", "warning")
            return
        
        item = self.movements_tree.item(selected[0])
        movement_id = int(item['values'][0])
        
        if messagebox.askyesno("Επιβεβαίωση", "Διαγραφή κίνησης;"):
            self.movements = [m for m in self.movements if m['id'] != movement_id]
            self.save_movements()
            self.refresh_all()
            # Ενημέρωση όλων των tabs άμεσα
            self.root.update_idletasks()
            self.show_notification("✓ Διαγράφηκε", "success")
    
    # Display Operations
    
    def format_number(self, num):
        """Format number to show integers without decimals, floats with decimals"""
        if isinstance(num, (int, float)):
            if num == int(num):
                return str(int(num))
            else:
                return str(num)
        return str(num)
    
    def refresh_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        search_term = self.search_var.get().lower()
        category_filter = self.category_filter.get() if hasattr(self, 'category_filter') else "Όλες"
        
        # Sort products alphabetically by name
        sorted_products = sorted(self.products, key=lambda x: x['name'].lower())
        
        display_idx = 0
        for idx, p in enumerate(sorted_products):
            # Search filter
            if search_term and search_term not in p['name'].lower() and search_term not in str(p.get('code', '')).lower():
                continue
            
            # Category filter
            if category_filter != "Όλες" and p.get('category', '⚡ Άλλο') != category_filter:
                continue
            
            display_idx += 1
            current_stock = self.get_current_stock(p['id'])
            status = "⚠️ ΧΑΜΗΛΟ" if current_stock < p['min_limit'] else "✓ OK"
            tag = "low" if current_stock < p['min_limit'] else "ok"
            row_tag = "evenrow" if display_idx % 2 == 0 else "oddrow"
            
            # Χρήση του πραγματικού ID σαν iid για να το ανακτήσουμε αργότερα
            self.products_tree.insert("", tk.END, iid=str(p['id']), values=(
                display_idx,
                p['name'],
                p.get('category', '⚡ Άλλο'),
                p.get('code', ''),
                self.format_number(p['initial_stock']),
                self.format_number(p['min_limit']),
                self.format_number(current_stock),
                status
            ), tags=(tag, row_tag))
    
    def refresh_movements(self):
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)
        
        filter_val = self.movement_filter.get() if hasattr(self, 'movement_filter') else "Όλες"
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
        for idx, m in enumerate(reversed(self.movements)):
            # Apply filters
            if filter_val == "Εισαγωγές" and m['type'] != 'in':
                continue
            if filter_val == "Εξαγωγές" and m['type'] != 'out':
                continue
            
            m_date = datetime.strptime(m['date'].split()[0], "%Y-%m-%d").date()
            if filter_val == "Σήμερα" and m_date != today:
                continue
            if filter_val == "Τελευταία 7 ημέρες" and m_date < week_ago:
                continue
            
            product_name = next((p['name'] for p in self.products if p['id'] == m['product_id']), "Άγνωστο")
            type_text = "📥 Εισαγωγή" if m['type'] == 'in' else "📤 Εξαγωγή"
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            
            self.movements_tree.insert("", tk.END, values=(
                m['id'],
                m['date'],
                product_name,
                type_text,
                self.format_number(m['quantity']),
                m.get('notes', '')
            ), tags=(row_tag,))
    
    def refresh_stock(self):
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        filter_val = self.stock_filter.get() if hasattr(self, 'stock_filter') else "Όλα"
        
        for idx, p in enumerate(self.products):
            product_id = p['id']
            total_in = sum(m['quantity'] for m in self.movements 
                          if m['product_id'] == product_id and m['type'] == 'in')
            total_out = sum(m['quantity'] for m in self.movements 
                           if m['product_id'] == product_id and m['type'] == 'out')
            current_stock = p['initial_stock'] + total_in - total_out
            status = "⚠️ ΧΑΜΗΛΟ" if current_stock < p['min_limit'] else "✓ OK"
            
            # Apply filter
            if filter_val == "Μόνο Χαμηλά" and current_stock >= p['min_limit']:
                continue
            if filter_val == "Μόνο OK" and current_stock < p['min_limit']:
                continue
            
            tag = "low" if current_stock < p['min_limit'] else "ok"
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            
            self.stock_tree.insert("", tk.END, values=(
                p['name'],
                p.get('code', ''),
                self.format_number(p['initial_stock']),
                self.format_number(total_in),
                self.format_number(total_out),
                self.format_number(current_stock),
                self.format_number(p['min_limit']),
                status
            ), tags=(tag, row_tag))
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics"""
        # Stats
        total_products = len(self.products)
        low_stock = sum(1 for p in self.products if self.get_current_stock(p['id']) < p['min_limit'])
        total_movements = len(self.movements)
        
        today = datetime.now().date()
        movements_today = sum(1 for m in self.movements 
                             if datetime.strptime(m['date'].split()[0], "%Y-%m-%d").date() == today)
        
        # Update window title with live stats
        self.root.title(f"Stock Manager Pro - {total_products} Προϊόντα | {low_stock} Χαμηλά | {total_movements} Κινήσεις")
        
        # Update top bar stats
        self.stat_products.value_label.config(text=str(int(total_products)))  # type: ignore
        self.stat_low.value_label.config(text=str(int(low_stock)))  # type: ignore
        self.stat_movements.value_label.config(text=str(int(total_movements)))  # type: ignore
        
        # Update cards
        self.card_total.value_label.config(text=str(int(total_products)))  # type: ignore
        self.card_stock_value.value_label.config(text=str(int(sum(self.get_current_stock(p['id']) for p in self.products))))  # type: ignore
        self.card_low_stock.value_label.config(text=str(int(low_stock)))  # type: ignore
        self.card_movements_today.value_label.config(text=str(int(movements_today)))  # type: ignore
        
        # Recent activity
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        for m in list(reversed(self.movements))[:10]:
            product_name = next((p['name'] for p in self.products if p['id'] == m['product_id']), "Άγνωστο")
            type_text = "📥 Εισαγωγή" if m['type'] == 'in' else "📤 Εξαγωγή"
            
            self.activity_tree.insert("", tk.END, values=(
                m['date'],
                product_name,
                type_text,
                self.format_number(m['quantity'])
            ))
    
    def refresh_all(self):
        self.refresh_products()
        self.refresh_movements()
        self.refresh_history()
        self.refresh_stock()
        self.refresh_dashboard()
        self.refresh_reports()
    
    def refresh_reports(self):
        """Refresh reports tab"""
        if not hasattr(self, 'report_total_products'):
            return
        
        # Basic stats
        total_products = len(self.products)
        total_movements = len(self.movements)
        
        # Calculate stock value (if products have price)
        stock_value = sum(
            self.get_current_stock(p['id']) * p.get('price', 0)
            for p in self.products
        )
        
        self.report_total_products.value_label.config(text=str(int(total_products)))  # type: ignore
        self.report_total_movements.value_label.config(text=str(int(total_movements)))  # type: ignore
        self.report_stock_value.value_label.config(text=f"{stock_value:.2f} €" if stock_value > 0 else "Χωρίς τιμές")  # type: ignore
        
        # Most active products
        for item in self.most_active_tree.get_children():
            self.most_active_tree.delete(item)
        
        product_activity = []
        for p in self.products:
            total_in = sum(m['quantity'] for m in self.movements 
                          if m['product_id'] == p['id'] and m['type'] == 'in')
            total_out = sum(m['quantity'] for m in self.movements 
                           if m['product_id'] == p['id'] and m['type'] == 'out')
            total_moves = total_in + total_out
            product_activity.append((p['name'], total_moves, total_in, total_out))
        
        # Sort by activity
        product_activity.sort(key=lambda x: x[1], reverse=True)
        
        for name, total, ins, outs in product_activity[:5]:
            self.most_active_tree.insert("", tk.END, values=(
                name,
                self.format_number(total),
                self.format_number(ins),
                self.format_number(outs)
            ))
        
        # Least active products
        for item in self.least_active_tree.get_children():
            self.least_active_tree.delete(item)
        
        for name, total, ins, outs in product_activity[-5:]:
            self.least_active_tree.insert("", tk.END, values=(
                name,
                self.format_number(total),
                self.format_number(ins),
                self.format_number(outs)
            ))
        
        # Monthly summary
        for item in self.monthly_tree.get_children():
            self.monthly_tree.delete(item)
        
        monthly_data = {}
        for m in self.movements:
            try:
                date = datetime.strptime(m['date'].split()[0], "%Y-%m-%d")
                month_key = date.strftime("%Y-%m")
                month_name = date.strftime("%m/%Y")
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = {'name': month_name, 'in': 0, 'out': 0, 'total': 0}
                
                if m['type'] == 'in':
                    monthly_data[month_key]['in'] += m['quantity']
                else:
                    monthly_data[month_key]['out'] += m['quantity']
                monthly_data[month_key]['total'] += 1
            except:
                pass
        
        for month_key in sorted(monthly_data.keys(), reverse=True)[:12]:
            data = monthly_data[month_key]
            self.monthly_tree.insert("", tk.END, values=(
                data['name'],
                self.format_number(data['in']),
                self.format_number(data['out']),
                self.format_number(data['total'])
            ))
    
    def refresh_history(self):
        """Refresh history tab with date filters"""
        if not hasattr(self, 'history_tree'):
            return
        
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get date range
        try:
            from_date_str = self.history_from_date.get()
            to_date_str = self.history_to_date.get()
            
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except:
            messagebox.showerror("Σφάλμα", "Μη έγκυρη μορφή ημερομηνίας!\nΧρησιμοποιήστε: YYYY-MM-DD")
            return
        
        # Filter movements by date
        filtered_movements = []
        for m in self.movements:
            try:
                movement_date = datetime.strptime(m['date'].split()[0], "%Y-%m-%d")
                if from_date <= movement_date <= to_date:
                    filtered_movements.append(m)
            except:
                pass
        
        # Sort by date (newest first)
        filtered_movements.sort(key=lambda x: x['date'], reverse=True)
        
        # Statistics
        total_in = sum(m['quantity'] for m in filtered_movements if m['type'] == 'in')
        total_out = sum(m['quantity'] for m in filtered_movements if m['type'] == 'out')
        
        # Display data
        for i, m in enumerate(filtered_movements):
            product = next((p for p in self.products if p['id'] == m['product_id']), None)
            if product:
                date_parts = m['date'].split()
                date_str = date_parts[0] if date_parts else m['date']
                time_str = date_parts[1] if len(date_parts) > 1 else "-"
                
                type_display = "📥 Εισαγωγή" if m['type'] == 'in' else "📤 Εξαγωγή"
                
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                
                self.history_tree.insert("", tk.END, values=(
                    m['id'],
                    date_str,
                    time_str,
                    product['name'],
                    product.get('category', '-'),
                    type_display,
                    self.format_number(m['quantity']),
                    m.get('notes', '')
                ), tags=(tag,))
        
        # Update summary
        self.history_summary_label.config(
            text=f"📊 Σύνολο κινήσεων: {len(filtered_movements)} | "
                 f"📥 Εισαγωγές: {self.format_number(total_in)} | "
                 f"📤 Εξαγωγές: {self.format_number(total_out)} | "
                 f"📅 Περίοδος: {from_date_str} έως {to_date_str}"
        )
    
    def export_history_to_excel(self):
        """Export history to Excel file"""
        try:
            from_date_str = self.history_from_date.get()
            to_date_str = self.history_to_date.get()
            
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except:
            messagebox.showerror("Σφάλμα", "Μη έγκυρη μορφή ημερομηνίας!")
            return
        
        # Filter and prepare data
        filtered_movements = []
        for m in self.movements:
            try:
                movement_date = datetime.strptime(m['date'].split()[0], "%Y-%m-%d")
                if from_date <= movement_date <= to_date:
                    product = next((p for p in self.products if p['id'] == m['product_id']), None)
                    if product:
                        date_parts = m['date'].split()
                        filtered_movements.append({
                            'ID': m['id'],
                            'Ημερομηνία': date_parts[0] if date_parts else m['date'],
                            'Ώρα': date_parts[1] if len(date_parts) > 1 else "-",
                            'Προϊόν': product['name'],
                            'Κατηγορία': product.get('category', '-'),
                            'Τύπος': 'Εισαγωγή' if m['type'] == 'in' else 'Εξαγωγή',
                            'Ποσότητα': m['quantity'],
                            'Σημειώσεις': m.get('notes', '')
                        })
            except:
                pass
        
        if not filtered_movements:
            messagebox.showwarning("Προσοχή", "Δεν βρέθηκαν κινήσεις για την επιλεγμένη περίοδο!")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"history_{from_date_str}_to_{to_date_str}.xlsx"
        )
        
        if filename:
            try:
                df = pd.DataFrame(filtered_movements)
                df.to_excel(filename, index=False, sheet_name="Ιστορικό Κινήσεων")
                
                messagebox.showinfo(
                    "✅ Επιτυχής Εξαγωγή",
                    f"Το ιστορικό εξήχθη επιτυχώς!\n\n"
                    f"📁 Αρχείο: {Path(filename).name}\n"
                    f"📊 Κινήσεις: {len(filtered_movements)}\n"
                    f"📅 Περίοδος: {from_date_str} - {to_date_str}"
                )
                self.show_notification("✓ Εξαγωγή σε Excel ολοκληρώθηκε", "success")
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Αποτυχία εξαγωγής:\n{e}")
                self.show_notification(f"✗ Σφάλμα εξαγωγής: {e}", "error")
    
    def export_history_to_pdf(self):
        """Export history to PDF file"""
        try:
            from_date_str = self.history_from_date.get()
            to_date_str = self.history_to_date.get()
            
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except:
            messagebox.showerror("Σφάλμα", "Μη έγκυρη μορφή ημερομηνίας!")
            return
        
        # Filter movements
        filtered_movements = []
        for m in self.movements:
            try:
                movement_date = datetime.strptime(m['date'].split()[0], "%Y-%m-%d")
                if from_date <= movement_date <= to_date:
                    product = next((p for p in self.products if p['id'] == m['product_id']), None)
                    if product:
                        filtered_movements.append((m, product))
            except:
                pass
        
        if not filtered_movements:
            messagebox.showwarning("Προσοχή", "Δεν βρέθηκαν κινήσεις για την επιλεγμένη περίοδο!")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"history_{from_date_str}_to_{to_date_str}.pdf"
        )
        
        if filename:
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import A4, landscape
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
                
                # Create PDF
                doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
                elements = []
                
                # Styles
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    textColor=colors.HexColor('#2c3e50'),
                    spaceAfter=30,
                    alignment=1  # Center
                )
                
                # Title
                elements.append(Paragraph("ΙΣΤΟΡΙΚΟ ΚΙΝΗΣΕΩΝ ΑΠΟΘΗΚΗΣ", title_style))
                elements.append(Paragraph(f"Περίοδος: {from_date_str} έως {to_date_str}", styles['Normal']))
                elements.append(Spacer(1, 0.3*inch))
                
                # Statistics
                total_in = sum(m[0]['quantity'] for m in filtered_movements if m[0]['type'] == 'in')
                total_out = sum(m[0]['quantity'] for m in filtered_movements if m[0]['type'] == 'out')
                
                stats_text = f"Σύνολο Κινήσεων: {len(filtered_movements)} | Εισαγωγές: {total_in} | Εξαγωγές: {total_out}"
                elements.append(Paragraph(stats_text, styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
                
                # Table data
                data = [['ID', 'Ημερομηνία', 'Προϊόν', 'Κατηγορία', 'Τύπος', 'Ποσότητα', 'Σημειώσεις']]
                
                for m, product in filtered_movements:
                    date_str = m['date'].split()[0]
                    type_str = 'Εισαγωγή' if m['type'] == 'in' else 'Εξαγωγή'
                    data.append([
                        str(m['id']),
                        date_str,
                        product['name'][:20],
                        product.get('category', '-')[:15],
                        type_str,
                        str(m['quantity']),
                        m.get('notes', '')[:25]
                    ])
                
                # Create table
                table = Table(data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white]),
                ]))
                
                elements.append(table)
                
                # Build PDF
                doc.build(elements)
                
                messagebox.showinfo(
                    "✅ Επιτυχής Εξαγωγή",
                    f"Το ιστορικό εξήχθη επιτυχώς σε PDF!\n\n"
                    f"📁 Αρχείο: {Path(filename).name}\n"
                    f"📊 Κινήσεις: {len(filtered_movements)}"
                )
                self.show_notification("✓ Εξαγωγή σε PDF ολοκληρώθηκε", "success")
            except ImportError:
                messagebox.showerror(
                    "Απαιτείται reportlab",
                    "Για εξαγωγή σε PDF απαιτείται η βιβλιοθήκη reportlab.\n\n"
                    "Εγκατάσταση: pip install reportlab"
                )
                self.show_notification("✗ Δεν βρέθηκε το reportlab", "error")
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Αποτυχία εξαγωγής PDF:\n{e}")
                self.show_notification(f"✗ Σφάλμα εξαγωγής: {e}", "error")
    
    def on_search(self, *args):
        """Handle search"""
        self.refresh_products()
    
    def auto_refresh_dashboard(self):
        """Αυτόματη ενημέρωση dashboard κάθε 30 δευτερόλεπτα"""
        try:
            self.refresh_dashboard()
        except:
            pass
        # Επανάληψη μετά από 30 δευτερόλεπτα
        self.root.after(30000, self.auto_refresh_dashboard)
    
    def on_closing(self):
        """Ασφαλής έξοδος με αποθήκευση"""
        if messagebox.askokcancel("Έξοδος", "Θέλετε να κλείσετε την εφαρμογή;\n\nΌλα τα δεδομένα θα αποθηκευτούν αυτόματα."):
            try:
                # Τελική αποθήκευση όλων
                self.save_products()
                self.save_movements()
                self.save_categories()
                
                # Τελικό backup
                self.auto_backup()
                
                print("✓ Όλα τα δεδομένα αποθηκεύτηκαν επιτυχώς!")
                self.root.destroy()
            except Exception as e:
                if messagebox.askyesno("Σφάλμα Αποθήκευσης", 
                                      f"Προέκυψε σφάλμα κατά την αποθήκευση:\n{e}\n\nΘέλετε να κλείσετε ούτως ή άλλως;"):
                    self.root.destroy()
        else:
            # Δεν κλείνει - συνεχίζει κανονικά
            pass
    
    def show_notification(self, message, type="info"):
        """Show notification in status bar"""
        colors = {
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'info': '#3498db'
        }
        self.status_bar.config(text=message, fg=colors.get(type, '#2c3e50'))
        self.root.after(3000, lambda: self.status_bar.config(text="✓ Έτοιμο", fg=self.colors['dark']))
    
    def export_to_excel(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                initialfile=f"apothema_{datetime.now().strftime('%Y%m%d')}.xlsx"
            )
            
            if filename:
                products_df = pd.DataFrame(self.products)
                movements_df = pd.DataFrame(self.movements)
                
                stock_data = []
                for p in self.products:
                    total_in = sum(m['quantity'] for m in self.movements 
                                  if m['product_id'] == p['id'] and m['type'] == 'in')
                    total_out = sum(m['quantity'] for m in self.movements 
                                   if m['product_id'] == p['id'] and m['type'] == 'out')
                    current_stock = p['initial_stock'] + total_in - total_out
                    stock_data.append({
                        'Προϊόν': p['name'],
                        'Κωδικός': p.get('code', ''),
                        'Αρχικό': p['initial_stock'],
                        'Εισαγωγές': total_in,
                        'Εξαγωγές': total_out,
                        'Τρέχον': current_stock,
                        'Ελάχιστο': p['min_limit'],
                        'Κατάσταση': "ΧΑΜΗΛΟ" if current_stock < p['min_limit'] else "OK"
                    })
                
                stock_df = pd.DataFrame(stock_data)
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    products_df.to_excel(writer, sheet_name='Προϊόντα', index=False)
                    movements_df.to_excel(writer, sheet_name='Κινήσεις', index=False)
                    stock_df.to_excel(writer, sheet_name='Απόθεμα', index=False)
                
                self.show_notification(f"✓ Εξήχθη: {Path(filename).name}", "success")
        except Exception as e:
            self.show_notification(f"✗ Σφάλμα: {e}", "error")
    
    def export_to_pdf(self):
        """Export stock report to PDF with Greek support"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=f"apothema_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
            
            if not filename:
                return
            
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            # Προσπάθεια εγκατάστασης ελληνικού font
            try:
                # Χρήση DejaVu Sans που υποστηρίζει ελληνικά
                import os
                font_path = None
                
                # Αναζήτηση για DejaVu Sans στο σύστημα
                possible_paths = [
                    "C:/Windows/Fonts/DejaVuSans.ttf",
                    "C:/Windows/Fonts/Arial.ttf",
                    "C:/Windows/Fonts/arialuni.ttf",
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        font_path = path
                        break
                
                if font_path:
                    pdfmetrics.registerFont(TTFont('GreekFont', font_path))
                    font_name = 'GreekFont'
                else:
                    font_name = 'Helvetica'
            except:
                font_name = 'Helvetica'
            
            doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
            elements = []
            
            # Τίτλος - χωρίς Paragraph για να αποφύγουμε προβλήματα
            from reportlab.platypus import PageBreak
            
            # Δεδομένα πίνακα με ASCII-safe headers
            data = [['#', 'Product', 'Category', 'Initial', 'In', 'Out', 'Current', 'Min', 'Status']]
            
            for idx, p in enumerate(self.products, 1):
                total_in = sum(m['quantity'] for m in self.movements 
                              if m['product_id'] == p['id'] and m['type'] == 'in')
                total_out = sum(m['quantity'] for m in self.movements 
                               if m['product_id'] == p['id'] and m['type'] == 'out')
                current_stock = p['initial_stock'] + total_in - total_out
                status = "LOW" if current_stock < p['min_limit'] else "OK"
                
                # Χρήση ASCII-safe strings
                product_name = p['name'][:35]
                category = p.get('category', '---')[:20]
                
                data.append([
                    str(idx),
                    product_name,
                    category,
                    str(p['initial_stock']),
                    str(total_in),
                    str(total_out),
                    str(current_stock),
                    str(p['min_limit']),
                    status
                ])
            
            # Δημιουργία πίνακα με μικρότερα font για να χωράνε περισσότερα
            col_widths = [0.4*inch, 2.2*inch, 1.3*inch, 0.6*inch, 0.5*inch, 0.5*inch, 0.7*inch, 0.6*inch, 0.7*inch]
            
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), font_name + '-Bold' if font_name == 'Helvetica' else font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ]))
            
            elements.append(table)
            
            doc.build(elements)
            
            # Μήνυμα επιτυχίας
            total_products = len(self.products)
            low_stock = sum(1 for p in self.products if self.get_current_stock(p['id']) < p['min_limit'])
            
            messagebox.showinfo(
                "✅ PDF Δημιουργήθηκε",
                f"Το PDF εξήχθη επιτυχώς!\n\n"
                f"📄 Αρχείο: {Path(filename).name}\n"
                f"📦 Προϊόντα: {total_products}\n"
                f"⚠️ Χαμηλά: {low_stock}\n"
                f"📋 Κινήσεις: {len(self.movements)}"
            )
            
            self.show_notification(f"✓ PDF εξήχθη: {Path(filename).name}", "success")
            
        except ImportError:
            messagebox.showerror(
                "Λείπει Βιβλιοθήκη",
                "Η βιβλιοθήκη 'reportlab' δεν είναι εγκατεστημένη!\n\n"
                "Εκτελέστε: pip install reportlab\n\n"
                "Χρησιμοποιήστε προσωρινά την εξαγωγή σε Excel."
            )
        except Exception as e:
            self.show_notification(f"✗ Σφάλμα PDF: {str(e)[:50]}", "error")
            messagebox.showerror("Σφάλμα", f"Πρόβλημα εξαγωγής PDF:\n{e}")


# Dialogs (same as before)

class ProductDialog:
    def __init__(self, parent, title, product=None, categories=None):
        self.result = None
        
        # Use provided categories or defaults
        if categories is None:
            categories = [
                "🍕 Τρόφιμα",
                "🍺 Ποτά", 
                "🧴 Καθαριστικά",
                "📦 Υλικά Συσκευασίας",
                "🔧 Εργαλεία",
                "📄 Γραφική Ύλη",
                "💊 Φαρμακευτικά",
                "🎨 Καλλυντικά",
                "🏠 Οικιακά Είδη",
                "⚡ Άλλο"
            ]
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x500")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg="#3498db", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📦 {title}",
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=18)
        
        # Form
        frame = tk.Frame(dialog, padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Όνομα Προϊόντος *", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=tk.W, pady=10)
        name_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        name_entry.grid(row=0, column=1, pady=10, ipady=4)
        
        tk.Label(frame, text="Κωδικός", font=("Segoe UI", 10)).grid(row=1, column=0, sticky=tk.W, pady=10)
        code_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        code_entry.grid(row=1, column=1, pady=10, ipady=4)
        
        tk.Label(frame, text="Κατηγορία *", font=("Segoe UI", 10)).grid(row=2, column=0, sticky=tk.W, pady=10)
        category_combo = ttk.Combobox(frame, font=("Segoe UI", 11), width=28, state="readonly")
        category_combo['values'] = categories
        category_combo.grid(row=2, column=1, pady=10)
        category_combo.current(9)  # Default to "⚡ Άλλο"
        
        tk.Label(frame, text="Αρχικό Απόθεμα *", font=("Segoe UI", 10)).grid(row=3, column=0, sticky=tk.W, pady=10)
        initial_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        initial_entry.grid(row=3, column=1, pady=10, ipady=4)
        
        tk.Label(frame, text="Ελάχιστο Όριο *", font=("Segoe UI", 10)).grid(row=4, column=0, sticky=tk.W, pady=10)
        min_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        min_entry.grid(row=4, column=1, pady=10, ipady=4)
        
        tk.Label(frame, text="Τιμή (€) (προαιρετικό)", font=("Segoe UI", 10)).grid(row=5, column=0, sticky=tk.W, pady=10)
        price_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        price_entry.grid(row=5, column=1, pady=10, ipady=4)
        
        if product:
            name_entry.insert(0, product['name'])
            code_entry.insert(0, product.get('code', ''))
            if product.get('category') in categories:
                category_combo.set(product.get('category'))
            initial_entry.insert(0, str(product['initial_stock']))
            min_entry.insert(0, str(product['min_limit']))
            if product.get('price'):
                price_entry.insert(0, str(product.get('price', '')))
        
        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def save():
            try:
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Σφάλμα", "Το όνομα είναι υποχρεωτικό!")
                    return
                
                self.result = {
                    'name': name,
                    'code': code_entry.get().strip(),
                    'category': category_combo.get(),
                    'initial_stock': int(float(initial_entry.get() or 0)),
                    'min_limit': int(float(min_entry.get() or 0)),
                    'price': float(price_entry.get() or 0) if price_entry.get().strip() else 0
                }
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Σφάλμα", "Μη έγκυρες τιμές!")
        
        ModernButton(
            btn_frame,
            text="💾 Αποθήκευση",
            command=save,
            bg="#27ae60",
            fg="white",
            padx=25,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="❌ Ακύρωση",
            command=dialog.destroy,
            bg="#e74c3c",
            fg="white",
            padx=25,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        name_entry.focus_set()
        dialog.wait_window()


class MovementDialog:
    def __init__(self, parent, movement_type, products):
        self.result = None
        
        title = "Εισαγωγή Προϊόντος" if movement_type == 'in' else "Εξαγωγή Προϊόντος"
        icon = "📥" if movement_type == 'in' else "📤"
        color = "#27ae60" if movement_type == 'in' else "#f39c12"
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x320")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg=color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"{icon} {title}",
            bg=color,
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=18)
        
        # Form
        frame = tk.Frame(dialog, padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Προϊόν *", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=tk.W, pady=10)
        product_combo = ttk.Combobox(frame, font=("Segoe UI", 11), width=28, state="readonly")
        product_combo['values'] = [p['name'] for p in products]
        product_combo.grid(row=0, column=1, pady=10)
        if products:
            product_combo.current(0)
        
        tk.Label(frame, text="Ποσότητα *", font=("Segoe UI", 10)).grid(row=1, column=0, sticky=tk.W, pady=10)
        qty_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        qty_entry.grid(row=1, column=1, pady=10, ipady=4)
        
        tk.Label(frame, text="Σημειώσεις", font=("Segoe UI", 10)).grid(row=2, column=0, sticky=tk.W, pady=10)
        notes_entry = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        notes_entry.grid(row=2, column=1, pady=10, ipady=4)
        
        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save():
            try:
                selected_product = product_combo.get()
                if not selected_product:
                    messagebox.showerror("Σφάλμα", "Επιλέξτε προϊόν!")
                    return
                
                quantity = float(qty_entry.get() or 0)
                
                product_id = next((p['id'] for p in products if p['name'] == selected_product), None)
                
                self.result = {
                    'product_id': product_id,
                    'type': movement_type,
                    'quantity': int(quantity),
                    'notes': notes_entry.get().strip()
                }
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Σφάλμα", "Μη έγκυρη ποσότητα!")
        
        ModernButton(
            btn_frame,
            text="💾 Καταχώριση",
            command=save,
            bg="#27ae60",
            fg="white",
            padx=25,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="❌ Ακύρωση",
            command=dialog.destroy,
            bg="#e74c3c",
            fg="white",
            padx=25,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        qty_entry.focus_set()
        dialog.wait_window()


class CategoryDialog:
    def __init__(self, parent, categories):
        self.result = None
        self.categories = categories.copy()
        
        dialog = tk.Toplevel(parent)
        dialog.title("Διαχείριση Κατηγοριών")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg="#9b59b6", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🏷️ Διαχείριση Κατηγοριών",
            bg="#9b59b6",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=18)
        
        # Content
        content = tk.Frame(dialog, padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # List of categories
        tk.Label(
            content,
            text="Κατηγορίες:",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        list_frame = tk.Frame(content)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.category_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            height=12
        )
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.category_listbox.yview)
        
        for cat in self.categories:
            self.category_listbox.insert(tk.END, cat)
        
        # Add new category
        add_frame = tk.Frame(content)
        add_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.new_category_entry = tk.Entry(
            add_frame,
            font=("Segoe UI", 11),
            width=35
        )
        self.new_category_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=4)
        self.new_category_entry.bind('<Return>', lambda e: add_category())
        
        def add_category():
            new_cat = self.new_category_entry.get().strip()
            if new_cat and new_cat not in self.categories:
                self.categories.append(new_cat)
                self.category_listbox.insert(tk.END, new_cat)
                self.new_category_entry.delete(0, tk.END)
            elif new_cat in self.categories:
                messagebox.showwarning("Προσοχή", "Η κατηγορία υπάρχει ήδη!")
        
        ModernButton(
            add_frame,
            text="➕ Προσθήκη",
            command=add_category,
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8
        ).pack(side=tk.LEFT)
        
        # Edit button
        def edit_category():
            selection = self.category_listbox.curselection()
            if not selection:
                messagebox.showwarning("Προσοχή", "Επιλέξτε μια κατηγορία για επεξεργασία!")
                return
            
            idx = selection[0]
            old_cat = self.categories[idx]
            
            # Δημιουργία dialog για επεξεργασία
            edit_dialog = tk.Toplevel(dialog)
            edit_dialog.title("Επεξεργασία Κατηγορίας")
            edit_dialog.geometry("400x150")
            edit_dialog.resizable(False, False)
            edit_dialog.transient(dialog)
            edit_dialog.grab_set()
            
            # Center dialog
            edit_dialog.update_idletasks()
            x = (edit_dialog.winfo_screenwidth() // 2) - (200)
            y = (edit_dialog.winfo_screenheight() // 2) - (75)
            edit_dialog.geometry(f"+{x}+{y}")
            
            tk.Label(
                edit_dialog,
                text="Νέο όνομα κατηγορίας:",
                font=("Segoe UI", 11)
            ).pack(padx=20, pady=(20, 10))
            
            edit_entry = tk.Entry(
                edit_dialog,
                font=("Segoe UI", 12),
                width=30
            )
            edit_entry.pack(padx=20, pady=5, ipady=4)
            edit_entry.insert(0, old_cat)
            edit_entry.select_range(0, tk.END)
            edit_entry.focus_set()
            
            def save_edit():
                new_cat = edit_entry.get().strip()
                if not new_cat:
                    messagebox.showwarning("Προσοχή", "Το όνομα δεν μπορεί να είναι κενό!")
                    return
                if new_cat != old_cat and new_cat in self.categories:
                    messagebox.showwarning("Προσοχή", "Η κατηγορία υπάρχει ήδη!")
                    return
                
                self.categories[idx] = new_cat
                self.category_listbox.delete(idx)
                self.category_listbox.insert(idx, new_cat)
                self.category_listbox.selection_set(idx)
                edit_dialog.destroy()
            
            edit_entry.bind('<Return>', lambda e: save_edit())
            
            btn_frame = tk.Frame(edit_dialog)
            btn_frame.pack(pady=15)
            
            ModernButton(
                btn_frame,
                text="💾 Αποθήκευση",
                command=save_edit,
                bg="#27ae60",
                fg="white",
                padx=20,
                pady=8
            ).pack(side=tk.LEFT, padx=5)
            
            ModernButton(
                btn_frame,
                text="❌ Ακύρωση",
                command=edit_dialog.destroy,
                bg="#95a5a6",
                fg="white",
                padx=20,
                pady=8
            ).pack(side=tk.LEFT, padx=5)
        
        # Delete button
        def delete_category():
            selection = self.category_listbox.curselection()
            if selection:
                idx = selection[0]
                cat = self.categories[idx]
                if messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή κατηγορίας '{cat}';"):
                    del self.categories[idx]
                    self.category_listbox.delete(idx)
        
        # Action buttons frame
        action_frame = tk.Frame(content)
        action_frame.pack(pady=(0, 15))
        
        ModernButton(
            action_frame,
            text="✏️ Επεξεργασία",
            command=edit_category,
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            action_frame,
            text="🗑️ Διαγραφή",
            command=delete_category,
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(content)
        btn_frame.pack()
        
        def save():
            if not self.categories:
                messagebox.showerror("Σφάλμα", "Πρέπει να υπάρχει τουλάχιστον μία κατηγορία!")
                return
            self.result = self.categories
            dialog.destroy()
        
        ModernButton(
            btn_frame,
            text="💾 Αποθήκευση",
            command=save,
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="❌ Ακύρωση",
            command=dialog.destroy,
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        self.new_category_entry.focus_set()
        dialog.wait_window()


class BackupRestoreDialog:
    def __init__(self, parent, backups):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Επαναφορά Backup")
        dialog.geometry("750x550")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg="#f39c12", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📥 Επαναφορά από Backup",
            bg="#f39c12",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=18)
        
        # Content
        content = tk.Frame(dialog, padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Info label
        info_frame = tk.Frame(content, bg="#e8f5e9", relief=tk.RAISED, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            info_frame,
            text="ℹ️ Επιλέξτε ένα backup για επαναφορά. Τα τρέχοντα δεδομένα θα αντικατασταθούν.",
            bg="#e8f5e9",
            fg="#2e7d32",
            font=("Segoe UI", 9),
            wraplength=650
        ).pack(pady=10, padx=10)
        
        tk.Label(
            content,
            text=f"Διαθέσιμα Backups ({len(backups)}):",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # List frame with details
        list_frame = tk.Frame(content)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview for better display
        columns = ("Ημερομηνία", "Ώρα", "Μέγεθος", "Προϊόντα", "Κινήσεις")
        tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=12
        )
        
        # Configure columns
        tree.column("Ημερομηνία", width=120, anchor=tk.CENTER)
        tree.column("Ώρα", width=100, anchor=tk.CENTER)
        tree.column("Μέγεθος", width=100, anchor=tk.CENTER)
        tree.column("Προϊόντα", width=100, anchor=tk.CENTER)
        tree.column("Κινήσεις", width=100, anchor=tk.CENTER)
        
        tree.heading("Ημερομηνία", text="📅 Ημερομηνία")
        tree.heading("Ώρα", text="🕐 Ώρα")
        tree.heading("Μέγεθος", text="💾 Μέγεθος")
        tree.heading("Προϊόντα", text="📦 Προϊόντα")
        tree.heading("Κινήσεις", text="📋 Κινήσεις")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add backups to tree with details
        for i, backup in enumerate(backups):
            timestamp = backup.stem.replace("backup_", "")
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                date_str = dt.strftime("%d/%m/%Y")
                time_str = dt.strftime("%H:%M:%S")
            except:
                date_str = timestamp
                time_str = "-"
            
            # Get file size
            size_kb = backup.stat().st_size / 1024
            if size_kb < 1024:
                size_str = f"{size_kb:.1f} KB"
            else:
                size_str = f"{size_kb/1024:.2f} MB"
            
            # Try to read backup details
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                    num_products = len(backup_data.get('products', []))
                    num_movements = len(backup_data.get('movements', []))
            except:
                num_products = "?"
                num_movements = "?"
            
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", tk.END, values=(
                date_str,
                time_str,
                size_str,
                num_products,
                num_movements
            ), tags=(tag,))
        
        tree.tag_configure("evenrow", background="#f5f5f5")
        tree.tag_configure("oddrow", background="white")
        
        self.tree = tree
        self.backups = backups
        
        # Details frame
        details_frame = tk.LabelFrame(
            content,
            text="📋 Λεπτομέρειες Επιλεγμένου Backup",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10
        )
        details_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.details_label = tk.Label(
            details_frame,
            text="Επιλέξτε ένα backup για να δείτε λεπτομέρειες",
            font=("Segoe UI", 9),
            fg="#7f8c8d",
            justify=tk.LEFT
        )
        self.details_label.pack(anchor=tk.W)
        
        def on_select(event):
            selection = tree.selection()
            if selection:
                idx = tree.index(selection[0])
                backup_file = self.backups[idx]
                
                try:
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                    
                    num_products = len(backup_data.get('products', []))
                    num_movements = len(backup_data.get('movements', []))
                    num_categories = len(backup_data.get('categories', []))
                    
                    timestamp = backup_file.stem.replace("backup_", "")
                    dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                    
                    details_text = (
                        f"📦 Προϊόντα: {num_products} | "
                        f"📋 Κινήσεις: {num_movements} | "
                        f"🏷️ Κατηγορίες: {num_categories}\n"
                        f"📅 Δημιουργήθηκε: {dt.strftime('%d/%m/%Y %H:%M:%S')}"
                    )
                    self.details_label.config(text=details_text, fg="#2c3e50")
                except:
                    self.details_label.config(
                        text="⚠️ Δεν ήταν δυνατή η ανάγνωση των λεπτομερειών",
                        fg="#e74c3c"
                    )
        
        tree.bind("<<TreeviewSelect>>", on_select)
        
        # Buttons
        btn_frame = tk.Frame(content)
        btn_frame.pack()
        
        def restore():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Προσοχή", "Επιλέξτε ένα backup!")
                return
            
            idx = tree.index(selection[0])
            backup_file = self.backups[idx]
            
            # Show confirmation with details
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                
                num_products = len(backup_data.get('products', []))
                num_movements = len(backup_data.get('movements', []))
                
                msg = (
                    "⚠️ ΠΡΟΣΟΧΗ ⚠️\n\n"
                    "Η επαναφορά θα αντικαταστήσει ΟΛΑ τα τρέχοντα δεδομένα!\n\n"
                    f"Το backup περιέχει:\n"
                    f"  • {num_products} προϊόντα\n"
                    f"  • {num_movements} κινήσεις\n\n"
                    "Θέλετε να συνεχίσετε;"
                )
            except:
                msg = (
                    "⚠️ ΠΡΟΣΟΧΗ ⚠️\n\n"
                    "Η επαναφορά θα αντικαταστήσει τα τρέχοντα δεδομένα.\n\n"
                    "Θέλετε να συνεχίσετε;"
                )
            
            if messagebox.askyesno("Επιβεβαίωση Επαναφοράς", msg):
                self.result = backup_file
                dialog.destroy()
        
        ModernButton(
            btn_frame,
            text="📥 Επαναφορά Επιλεγμένου",
            command=restore,
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame,
            text="❌ Ακύρωση",
            command=dialog.destroy,
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=12
        ).pack(side=tk.LEFT, padx=5)
        
        dialog.wait_window()


def main():
    root = tk.Tk()
    app = StockManagerPro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
