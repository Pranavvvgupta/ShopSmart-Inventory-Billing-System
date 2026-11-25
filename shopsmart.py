"""
================================================================================
ShopSmart: Inventory and Billing System with Sales Analysis for Small Shops
Course: Computational Thinking and Programming (2026CSAE100) — Milestone 2
================================================================================
Team Members & Module Responsibilities:
1. Rishi Kumar (S26CSEU0295)         - Inventory Management & CSV Persistence
2. Pranav Gupta (S26CSEU0676)        - Billing Module & Input Validation
3. Harsh Sharma (S26CSEU0010)        - Sales Analysis (Ranking & Slow-Moving)
4. Gyan Amritya Thakur (S26CSEU3275) - Reports, Low-Stock Alerts, Charts & Main Menu
================================================================================
"""

import csv
import os
import sys
from datetime import datetime, timedelta

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False

# Always save/load CSVs in the exact folder where shopsmart.py is located on Windows
SCRIPT_DIR = (
    os.path.dirname(os.path.abspath(__file__))
    if "__file__" in globals()
    else os.getcwd()
)
INVENTORY_FILE = os.path.join(SCRIPT_DIR, "inventory.csv")
SALES_FILE = os.path.join(SCRIPT_DIR, "sales.csv")
REPORT_FILE = os.path.join(SCRIPT_DIR, "sales_report.txt")
CHART_FILE = os.path.join(SCRIPT_DIR, "top_selling_chart.png")

INVENTORY_FIELDS = ["item_id", "name", "category", "price", "quantity", "reorder_level"]
SALES_FIELDS = [
    "sale_id",
    "timestamp",
    "item_id",
    "name",
    "category",
    "unit_price",
    "quantity",
    "line_total",
]
SLOW_MOVING_DAYS = 30
SLOW_MOVING_THRESHOLD = 10


def pause_screen():
    """Pause on Windows/Terminal so the table stays on screen until Enter is pressed."""
    try:
        input("\n[Press Enter to return to the Main Menu...]")
    except EOFError:
        pass


# ==============================================================================
# EXPERIENTIAL LEARNING ACTIVITY 6: OBJECT MODELING (CLASSES & INHERITANCE)
# ==============================================================================


class Item:
    """Base class representing a retail shop inventory item (Encapsulation)."""

    def __init__(self, item_id, name, category, price, quantity, reorder_level):
        self.item_id = str(item_id).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self._price = float(price)
        self._quantity = int(quantity)
        self.reorder_level = int(reorder_level)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if float(new_price) <= 0:
            raise ValueError("Price must be greater than 0.")
        self._price = float(new_price)

    @property
    def quantity(self):
        return self._quantity

    def add_stock(self, units):
        if int(units) < 0:
            raise ValueError("Cannot add negative stock.")
        self._quantity += int(units)

    def deduct_stock(self, units):
        units = int(units)
        if units <= 0 or units > self._quantity:
            return False
        self._quantity -= units
        return True

    def is_low_stock(self):
        return self._quantity <= self.reorder_level

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "price": self._price,
            "quantity": self._quantity,
            "reorder_level": self.reorder_level,
        }


class GroceryItem(Item):
    """Subclass representing fast-moving grocery items (Inheritance & Polymorphism)."""

    def __init__(
        self, item_id, name, price, quantity, reorder_level, unit_label="kg/pack"
    ):
        super().__init__(item_id, name, "Grocery", price, quantity, reorder_level)
        self.unit_label = unit_label

    def is_low_stock(self):
        return super().is_low_stock()


# ==============================================================================
# MODULE 1: INVENTORY MANAGEMENT & CSV PERSISTENCE (Rishi Kumar - S26CSEU0295)
# ==============================================================================


def create_sample_files(reference_date=None, force_inventory=False, force_sales=False):
    """Create sample inventory.csv and sales.csv if they do not exist or are corrupted."""
    if reference_date is None:
        reference_date = datetime.now()

    if force_inventory or not os.path.exists(INVENTORY_FILE):
        sample_inventory = [
            ["101", "Rice 1kg", "Grocery", "60.00", "42", "10"],
            ["102", "Sugar 1kg", "Grocery", "45.00", "28", "10"],
            ["103", "Notebook A4", "Stationery", "40.00", "19", "8"],
            ["104", "Ball Pen Blue", "Stationery", "10.00", "85", "20"],
            ["105", "Bath Soap", "Personal Care", "35.00", "9", "10"],
            ["106", "Wheat Flour 5kg", "Grocery", "210.00", "7", "8"],
            ["107", "Cooking Oil 1L", "Grocery", "140.00", "18", "6"],
            ["108", "Highlighter", "Stationery", "25.00", "5", "8"],
            ["109", "Herbal Shampoo", "Personal Care", "95.00", "14", "5"],
            ["110", "Masala Tea 250g", "Grocery", "80.00", "22", "8"],
        ]
        with open(INVENTORY_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(INVENTORY_FIELDS)
            writer.writerows(sample_inventory)

    if force_sales or not os.path.exists(SALES_FILE):
        d = reference_date
        sample_sales = [
            [
                "S1001",
                (d - timedelta(days=35)).strftime("%Y-%m-%d 10:15"),
                "101",
                "Rice 1kg",
                "Grocery",
                "60.00",
                "12",
                "720.00",
            ],
            [
                "S1002",
                (d - timedelta(days=32)).strftime("%Y-%m-%d 14:20"),
                "104",
                "Ball Pen Blue",
                "Stationery",
                "10.00",
                "30",
                "300.00",
            ],
            [
                "S1003",
                (d - timedelta(days=25)).strftime("%Y-%m-%d 11:05"),
                "101",
                "Rice 1kg",
                "Grocery",
                "60.00",
                "28",
                "1680.00",
            ],
            [
                "S1004",
                (d - timedelta(days=21)).strftime("%Y-%m-%d 16:40"),
                "102",
                "Sugar 1kg",
                "Grocery",
                "45.00",
                "22",
                "990.00",
            ],
            [
                "S1005",
                (d - timedelta(days=18)).strftime("%Y-%m-%d 12:30"),
                "106",
                "Wheat Flour 5kg",
                "Grocery",
                "210.00",
                "15",
                "3150.00",
            ],
            [
                "S1006",
                (d - timedelta(days=14)).strftime("%Y-%m-%d 17:10"),
                "104",
                "Ball Pen Blue",
                "Stationery",
                "10.00",
                "45",
                "450.00",
            ],
            [
                "S1007",
                (d - timedelta(days=11)).strftime("%Y-%m-%d 10:50"),
                "107",
                "Cooking Oil 1L",
                "Grocery",
                "140.00",
                "14",
                "1960.00",
            ],
            [
                "S1008",
                (d - timedelta(days=8)).strftime("%Y-%m-%d 15:25"),
                "103",
                "Notebook A4",
                "Stationery",
                "40.00",
                "16",
                "640.00",
            ],
            [
                "S1009",
                (d - timedelta(days=5)).strftime("%Y-%m-%d 18:00"),
                "110",
                "Masala Tea 250g",
                "Grocery",
                "80.00",
                "12",
                "960.00",
            ],
            [
                "S1010",
                (d - timedelta(days=3)).strftime("%Y-%m-%d 11:45"),
                "105",
                "Bath Soap",
                "Personal Care",
                "35.00",
                "8",
                "280.00",
            ],
            [
                "S1011",
                (d - timedelta(days=2)).strftime("%Y-%m-%d 13:15"),
                "108",
                "Highlighter",
                "Stationery",
                "25.00",
                "3",
                "75.00",
            ],
            [
                "S1012",
                (d - timedelta(days=1)).strftime("%Y-%m-%d 19:05"),
                "109",
                "Herbal Shampoo",
                "Personal Care",
                "95.00",
                "4",
                "380.00",
            ],
            [
                "S1013",
                d.strftime("%Y-%m-%d 09:30"),
                "101",
                "Rice 1kg",
                "Grocery",
                "60.00",
                "10",
                "600.00",
            ],
            [
                "S1014",
                d.strftime("%Y-%m-%d 11:20"),
                "102",
                "Sugar 1kg",
                "Grocery",
                "45.00",
                "8",
                "360.00",
            ],
            [
                "S1015",
                d.strftime("%Y-%m-%d 14:10"),
                "103",
                "Notebook A4",
                "Stationery",
                "40.00",
                "5",
                "200.00",
            ],
        ]
        with open(SALES_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(SALES_FIELDS)
            writer.writerows(sample_sales)


def load_inventory():
    """Read inventory.csv into a dictionary keyed by item_id (handles Windows Excel BOM)."""
    inventory = {}
    if not os.path.exists(INVENTORY_FILE):
        create_sample_files(force_inventory=True)
    try:
        with open(INVENTORY_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row:
                    continue
                clean = {
                    str(k).strip().lower(): str(v).strip()
                    for k, v in row.items()
                    if k is not None and v is not None
                }
                item_id = clean.get("item_id", "")
                if not item_id:
                    continue
                inventory[item_id] = {
                    "name": clean.get("name", "Unknown Item"),
                    "category": clean.get("category", "General"),
                    "price": float(clean.get("price", 0.0)),
                    "quantity": int(float(clean.get("quantity", 0))),
                    "reorder_level": int(float(clean.get("reorder_level", 5))),
                }
    except Exception:
        create_sample_files(force_inventory=True)
        return load_inventory()

    if not inventory:
        create_sample_files(force_inventory=True)
        return load_inventory()
    return inventory


def save_inventory(inventory):
    """Write the updated inventory dictionary back to inventory.csv."""
    with open(INVENTORY_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(INVENTORY_FIELDS)
        for item_id in sorted(inventory.keys()):
            d = inventory[item_id]
            writer.writerow(
                [
                    item_id,
                    d["name"],
                    d["category"],
                    f"{d['price']:.2f}",
                    d["quantity"],
                    d["reorder_level"],
                ]
            )


def show_inventory(inventory):
    """Display formatted inventory table with stock status."""
    print(
        f"\n{'ID':<6}{'Name':<18}{'Category':<15}{'Price(Rs)':>10}{'Qty':>6}{'Reorder':>9}{'Status':>10}"
    )
    print("-" * 74)
    for item_id in sorted(inventory.keys()):
        d = inventory[item_id]
        status = "LOW!" if d["quantity"] <= d["reorder_level"] else "OK"
        print(
            f"{item_id:<6}{d['name']:<18}{d['category']:<15}"
            f"{d['price']:>10.2f}{d['quantity']:>6}{d['reorder_level']:>9}{status:>10}"
        )
    print("-" * 74)


def add_or_update_item(inventory):
    """Add a new item or update stock/price of an existing item."""
    item_id = input("Enter Item ID (e.g., 111): ").strip()
    if not item_id:
        print("  Item ID cannot be empty.")
        return

    if item_id in inventory:
        item = inventory[item_id]
        print(
            f"  Updating existing item: {item['name']} (Current Qty: {item['quantity']}, Price: Rs.{item['price']:.2f})"
        )
        add_qty = read_non_negative_int(
            "  Additional quantity to add (0 for no change): "
        )
        new_price = read_positive_float(
            f"  New unit price (Enter {item['price']:.2f} to keep unchanged): "
        )
        item["quantity"] += add_qty
        item["price"] = new_price
        save_inventory(inventory)
        print(
            f"  Updated '{item['name']}' -> Qty: {item['quantity']}, Price: Rs.{item['price']:.2f}"
        )
    else:
        name = input("  Enter Item Name: ").strip()
        category = (
            input("  Enter Category (Grocery/Stationery/Personal Care): ").strip()
            or "General"
        )
        price = read_positive_float("  Enter Unit Price (Rs.): ")
        quantity = read_positive_int("  Enter Opening Stock Quantity: ")
        reorder = read_positive_int("  Enter Reorder Alert Level: ")
        new_obj = (
            GroceryItem(item_id, name, price, quantity, reorder)
            if category.lower() == "grocery"
            else Item(item_id, name, category, price, quantity, reorder)
        )
        inventory[item_id] = new_obj.to_dict()
        save_inventory(inventory)
        print(f"  Added new item '{name}' (ID: {item_id}) to inventory.")


def delete_item(inventory):
    """Remove an item from inventory by item_id."""
    item_id = input("Enter Item ID to delete: ").strip()
    if item_id in inventory:
        removed = inventory.pop(item_id)
        save_inventory(inventory)
        print(f"  Deleted '{removed['name']}' (ID {item_id}) from inventory.")
    else:
        print("  Item ID not found.")


def search_inventory(inventory):
    """Search inventory by ID, partial item name, or category."""
    query = input("Enter search keyword (ID, Name, or Category): ").strip().lower()
    matches = {
        iid: d
        for iid, d in inventory.items()
        if query in iid.lower()
        or query in d["name"].lower()
        or query in d["category"].lower()
    }
    if not matches:
        print(f"  No matching items found for '{query}'.")
    else:
        print(f"\nFound {len(matches)} matching item(s):")
        show_inventory(matches)


# ==============================================================================
# MODULE 2: BILLING & INPUT VALIDATION (Pranav Gupta - S26CSEU0676)
# ==============================================================================


def read_positive_int(prompt):
    """Keep asking until the user enters a positive integer (> 0)."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("  Invalid input! Please enter a whole number greater than 0.")


def read_non_negative_int(prompt):
    """Keep asking until the user enters a non-negative integer (>= 0)."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) >= 0:
            return int(text)
        print("  Invalid input! Please enter 0 or a positive whole number.")


def read_positive_float(prompt):
    """Keep asking until the user enters a valid positive number (> 0)."""
    while True:
        text = input(prompt).strip()
        try:
            val = float(text)
            if val > 0:
                return val
        except ValueError:
            pass
        print("  Invalid input! Please enter a numeric value greater than 0.")


def log_sale_rows(cart, timestamp_str):
    """Append billed cart items to sales.csv with unique sale ID."""
    existing_count = 1000
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, newline="", encoding="utf-8-sig") as f:
            existing_count += sum(1 for _ in csv.DictReader(f))
    sale_id = f"S{existing_count + 1}"

    file_exists = os.path.exists(SALES_FILE)
    with open(SALES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(SALES_FIELDS)
        for item_id, name, category, price, qty, line_total in cart:
            writer.writerow(
                [
                    sale_id,
                    timestamp_str,
                    item_id,
                    name,
                    category,
                    f"{price:.2f}",
                    qty,
                    f"{line_total:.2f}",
                ]
            )
    return sale_id


def create_bill(inventory):
    """Build a multi-item customer bill, validate stock, update CSVs, and print receipt."""
    cart = []
    print("\n--- Create Customer Bill ---")
    print("Enter Item ID and quantity. Type 'done' as Item ID to finish.")

    while True:
        item_id = input("Item ID (or 'done'): ").strip()
        if item_id.lower() == "done":
            break
        if item_id not in inventory:
            print("  Error: Item ID not found in inventory. Try again.")
            continue

        item = inventory[item_id]
        if item["quantity"] == 0:
            print(f"  Alert: '{item['name']}' is currently out of stock!")
            continue

        qty = read_positive_int(
            f"Quantity of {item['name']} (Available: {item['quantity']}): "
        )
        if qty > item["quantity"]:
            print(
                f"  Error: Insufficient stock! Only {item['quantity']} unit(s) available."
            )
            continue

        item["quantity"] -= qty
        line_total = item["price"] * qty
        cart.append(
            (item_id, item["name"], item["category"], item["price"], qty, line_total)
        )
        print(
            f"  Added: {qty} x {item['name']} @ Rs.{item['price']:.2f} = Rs.{line_total:.2f}"
        )

    if not cart:
        print("No items billed.")
        return

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    sale_id = log_sale_rows(cart, timestamp_str)
    save_inventory(inventory)

    total = sum(line[5] for line in cart)
    total_units = sum(line[4] for line in cart)

    print("\n" + "=" * 52)
    print(f"SHOPSMART RETAIL RECEIPT | Bill ID: {sale_id}")
    print(f"Date & Time: {timestamp_str}")
    print("=" * 52)
    print(f"{'Item Name':<18}{'Qty':>5}{'Unit(Rs)':>12}{'Subtotal(Rs)':>15}")
    print("-" * 52)
    for _, name, _, price, qty, line_total in cart:
        print(f"{name:<18}{qty:>5}{price:>12.2f}{line_total:>15.2f}")
    print("-" * 52)
    print(f"{'Total Units:':<18}{total_units:>5}{'GRAND TOTAL:':>14} Rs.{total:>9.2f}")
    print("=" * 52)


# ==============================================================================
# MODULE 3: LOW-STOCK ALERTS (Gyan Amritya Thakur - S26CSEU3275)
# ==============================================================================


def low_stock_alert(inventory):
    """Identify and display items whose quantity is at or below reorder_level."""
    low_items = [
        (item_id, d)
        for item_id, d in sorted(inventory.items())
        if d["quantity"] <= d["reorder_level"]
    ]
    if not low_items:
        print(
            "\n[OK] All inventory items are sufficiently stocked above reorder levels."
        )
        return low_items

    print("\n" + "!" * 64)
    print("LOW STOCK REORDER ALERT (Quantity <= Reorder Level)")
    print("!" * 64)
    print(
        f"{'ID':<6}{'Item Name':<18}{'Category':<15}{'In Stock':>10}{'Reorder Lvl':>13}"
    )
    print("-" * 64)
    for item_id, d in low_items:
        print(
            f"{item_id:<6}{d['name']:<18}{d['category']:<15}{d['quantity']:>10}{d['reorder_level']:>13}"
        )
    print("-" * 64)
    return low_items


# ==============================================================================
# MODULE 4: SALES ANALYSIS - COMPUTATIONAL FEATURE (Harsh Sharma - S26CSEU0010)
# ==============================================================================


def load_sales():
    """Load all logged sales rows from sales.csv."""
    sales = []
    if not os.path.exists(SALES_FILE):
        create_sample_files(force_sales=True)
    try:
        with open(SALES_FILE, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if not row:
                    continue
                clean = {
                    str(k).strip().lower(): str(v).strip()
                    for k, v in row.items()
                    if k is not None and v is not None
                }
                if not clean.get("item_id"):
                    continue
                sales.append(
                    {
                        "sale_id": clean.get("sale_id", "S0000"),
                        "timestamp": clean.get("timestamp", ""),
                        "item_id": clean["item_id"],
                        "name": clean.get("name", "Unknown"),
                        "category": clean.get("category", "General"),
                        "unit_price": float(clean.get("unit_price", 0.0)),
                        "quantity": int(float(clean.get("quantity", 0))),
                        "line_total": float(clean.get("line_total", 0.0)),
                    }
                )
    except Exception:
        create_sample_files(force_sales=True)
        return load_sales()
    return sales


def analyze_sales(inventory, reference_date=None):
    """Rank items by revenue/units, flag 30-day slow movers, and summarize categories."""
    if reference_date is None:
        reference_date = datetime.now()
    cutoff_date = reference_date - timedelta(days=SLOW_MOVING_DAYS)

    sales = load_sales()
    item_stats = {}
    for iid, d in inventory.items():
        item_stats[iid] = {
            "name": d["name"],
            "category": d["category"],
            "total_units": 0,
            "units_30d": 0,
            "revenue": 0.0,
        }

    category_stats = {}

    for row in sales:
        iid = row["item_id"]
        qty = row["quantity"]
        rev = row["line_total"]
        cat = row["category"]

        try:
            sale_dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M")
        except ValueError:
            sale_dt = reference_date

        if iid not in item_stats:
            item_stats[iid] = {
                "name": row["name"],
                "category": cat,
                "total_units": 0,
                "units_30d": 0,
                "revenue": 0.0,
            }

        item_stats[iid]["total_units"] += qty
        item_stats[iid]["revenue"] += rev
        if sale_dt >= cutoff_date:
            item_stats[iid]["units_30d"] += qty

        if cat not in category_stats:
            category_stats[cat] = {"units": 0, "revenue": 0.0}
        category_stats[cat]["units"] += qty
        category_stats[cat]["revenue"] += rev

    ranked_by_revenue = sorted(
        item_stats.items(),
        key=lambda x: (x[1]["revenue"], x[1]["total_units"]),
        reverse=True,
    )
    ranked_by_units = sorted(
        item_stats.items(),
        key=lambda x: (x[1]["total_units"], x[1]["revenue"]),
        reverse=True,
    )

    slow_moving = [
        (iid, stats)
        for iid, stats in sorted(item_stats.items())
        if stats["units_30d"] < SLOW_MOVING_THRESHOLD
    ]

    return {
        "ranked_by_revenue": ranked_by_revenue,
        "ranked_by_units": ranked_by_units,
        "slow_moving": slow_moving,
        "category_stats": category_stats,
        "total_revenue": sum(s["revenue"] for s in item_stats.values()),
        "total_units": sum(s["total_units"] for s in item_stats.values()),
    }


def display_sales_analysis(inventory, reference_date=None):
    """Print ranked sales tables, slow-moving alerts, and category breakdown."""
    results = analyze_sales(inventory, reference_date=reference_date)

    print("\n=== 1. ITEM RANKING BY REVENUE & UNITS SOLD ===")
    print(
        f"{'Rank':<6}{'ID':<6}{'Item Name':<18}{'Category':<15}{'Units':>7}{'30d Units':>11}{'Revenue(Rs)':>14}"
    )
    print("-" * 77)
    for idx, (iid, st) in enumerate(results["ranked_by_revenue"], start=1):
        print(
            f"{idx:<6}{iid:<6}{st['name']:<18}{st['category']:<15}"
            f"{st['total_units']:>7}{st['units_30d']:>11}{st['revenue']:>14.2f}"
        )
    print("-" * 77)

    print(
        f"\n=== 2. SLOW-MOVING ITEMS (< {SLOW_MOVING_THRESHOLD} units in last {SLOW_MOVING_DAYS} days) ==="
    )
    if not results["slow_moving"]:
        print("  No slow-moving items detected.")
    else:
        for iid, st in results["slow_moving"]:
            print(
                f"  [SLOW] {st['name']} (ID {iid}, {st['category']}): "
                f"{st['units_30d']} units in last 30 days | Total Revenue: Rs.{st['revenue']:.2f}"
            )

    print("\n=== 3. CATEGORY-WISE PERFORMANCE SUMMARY ===")
    print(f"{'Category':<18}{'Units Sold':>12}{'Revenue(Rs)':>15}{'Revenue Share':>15}")
    print("-" * 60)
    grand_rev = results["total_revenue"] or 1.0
    for cat, cst in sorted(
        results["category_stats"].items(), key=lambda x: x[1]["revenue"], reverse=True
    ):
        share = (cst["revenue"] / grand_rev) * 100
        print(f"{cat:<18}{cst['units']:>12}{cst['revenue']:>15.2f}{share:>14.1f}%")
    print("-" * 60)
    return results


# ==============================================================================
# MODULE 5: REPORTS & MATPLOTLIB VISUALIZATION (Gyan Amritya Thakur - S26CSEU3275)
# ==============================================================================


def generate_sales_report(inventory, reference_date=None):
    """Generate daily and monthly revenue summaries, print to screen, and save to TXT."""
    sales = load_sales()
    results = analyze_sales(inventory, reference_date=reference_date)

    daily_totals = {}
    monthly_totals = {}
    for row in sales:
        day_key = row["timestamp"][:10]
        month_key = row["timestamp"][:7]
        daily_totals[day_key] = daily_totals.get(day_key, 0.0) + row["line_total"]
        monthly_totals[month_key] = (
            monthly_totals.get(month_key, 0.0) + row["line_total"]
        )

    lines = [
        "=" * 68,
        "SHOPSMART: DAILY & MONTHLY SALES ANALYSIS REPORT",
        f"Generated On: {(reference_date or datetime.now()).strftime('%Y-%m-%d %H:%M')}",
        "=" * 68,
        f"Total Cumulative Units Sold : {results['total_units']} units",
        f"Total Cumulative Revenue    : Rs. {results['total_revenue']:.2f}",
        "",
        "1. MONTHLY REVENUE SUMMARY",
        "-" * 40,
    ]
    for m_key, m_rev in sorted(monthly_totals.items()):
        lines.append(f"  Month {m_key:<12} : Rs. {m_rev:>10.2f}")

    lines.extend(["", "2. DAILY REVENUE SUMMARY", "-" * 40])
    for d_key, d_rev in sorted(daily_totals.items()):
        lines.append(f"  Date  {d_key:<12} : Rs. {d_rev:>10.2f}")

    lines.extend(["", "3. TOP-SELLING ITEMS BY REVENUE", "-" * 40])
    for idx, (iid, st) in enumerate(results["ranked_by_revenue"][:5], start=1):
        lines.append(
            f"  #{idx} {st['name']:<18} (ID {iid}) : {st['total_units']:>3} units | Rs. {st['revenue']:>8.2f}"
        )

    lines.extend(["", "4. SLOW-MOVING & LOW-STOCK ACTION ITEMS", "-" * 40])
    for iid, st in results["slow_moving"]:
        lines.append(
            f"  Slow-Moving : {st['name']} (ID {iid}) -> {st['units_30d']} units in last 30 days"
        )
    for iid, d in sorted(inventory.items()):
        if d["quantity"] <= d["reorder_level"]:
            lines.append(
                f"  Low-Stock   : {d['name']} (ID {iid}) -> {d['quantity']} left (Reorder at {d['reorder_level']})"
            )
    lines.append("=" * 68)

    report_text = "\n".join(lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")

    print("\n" + report_text)
    print(f"\n[Saved] Report successfully exported to '{REPORT_FILE}'.")
    return report_text


def generate_sales_chart(inventory, output_path=None):
    """Plot a Matplotlib bar chart of top-selling items by revenue and units."""
    if not MATPLOTLIB_AVAILABLE:
        print(
            "\n[Note] Matplotlib is not installed (run 'pip install matplotlib' in Command Prompt if needed)."
        )
        return None

    target_path = output_path or CHART_FILE
    results = analyze_sales(inventory)
    ranked = results["ranked_by_revenue"]

    names = [st["name"] for _, st in ranked]
    revenues = [st["revenue"] for _, st in ranked]
    units = [st["total_units"] for _, st in ranked]

    plt.rcParams.update({"font.size": 10})
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=220)
    bars = ax.barh(
        names[::-1], revenues[::-1], color="#1e3a5f", edgecolor="#0f172a", height=0.62
    )
    ax.set_xlabel("Cumulative Revenue (Rs.)", fontweight="bold", color="#1f2937")
    ax.set_title(
        "ShopSmart: Item-Wise Revenue & Unit Sales Performance",
        fontweight="bold",
        color="#1e3a5f",
        pad=10,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.margins(x=0.22)

    for bar, u in zip(bars, units[::-1]):
        w = bar.get_width()
        ax.text(
            w + 35,
            bar.get_y() + bar.get_height() / 2,
            f"Rs.{w:,.0f} ({u}u)",
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
            color="#1f2937",
        )

    fig.tight_layout()
    fig.savefig(target_path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"[Saved] Bar chart of top-selling items saved to '{target_path}'.")
    return target_path


# ==============================================================================
# MAIN MENU & APPLICATION CONTROLLER
# ==============================================================================


def main():
    create_sample_files()
    inventory = load_inventory()

    while True:
        print("\n==========================================")
        print("   SHOPSMART: INVENTORY & BILLING SYSTEM  ")
        print("==========================================")
        print("1. View Inventory")
        print("2. Add / Update Inventory Item")
        print("3. Delete / Search Inventory Item")
        print("4. Create Customer Bill")
        print("5. View Low-Stock Alerts")
        print("6. Run Sales Analysis (Ranking & Slow-Moving)")
        print("7. Generate TXT Report & Matplotlib Chart")
        print("8. Exit")

        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            show_inventory(inventory)
            pause_screen()
        elif choice == "2":
            add_or_update_item(inventory)
            pause_screen()
        elif choice == "3":
            sub = input("Enter 'S' to Search or 'D' to Delete: ").strip().upper()
            if sub == "D":
                delete_item(inventory)
            else:
                search_inventory(inventory)
            pause_screen()
        elif choice == "4":
            create_bill(inventory)
            pause_screen()
        elif choice == "5":
            low_stock_alert(inventory)
            pause_screen()
        elif choice == "6":
            display_sales_analysis(inventory)
            pause_screen()
        elif choice == "7":
            generate_sales_report(inventory)
            generate_sales_chart(inventory)
            pause_screen()
        elif choice == "8":
            print("Saving data and exiting ShopSmart. Goodbye!")
            save_inventory(inventory)
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[Unexpected Error] {e}")
        input("\nPress Enter to close window...")
