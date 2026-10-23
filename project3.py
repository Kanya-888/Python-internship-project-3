

import csv
import os
from datetime import datetime
from collections import defaultdict

FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]

CATEGORIES = ["Food", "Travel", "Study", "Bills", "Fun", "Other"]


def ensure_file():
    """Create the CSV file with a header if it does not exist."""
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def load_expenses():
    """Load all expense records from the CSV file."""
    ensure_file()

    try:
        with open(FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except (OSError, csv.Error) as error:
        print(f"Could not read expenses: {error}")
        return []


def save_expense(expense):
    """Append one expense to the CSV file."""
    ensure_file()

    try:
        with open(FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writerow(expense)
        print("Expense saved successfully!")
    except (OSError, csv.Error) as error:
        print(f"Could not save expense: {error}")


def get_valid_date():
    """Ask for a date in YYYY-MM-DD format."""
    while True:
        date_text = input("Date (YYYY-MM-DD): ").strip()

        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d")

            # Ensure the entered date uses the exact required format
            if parsed_date.strftime("%Y-%m-%d") != date_text:
                raise ValueError

            if parsed_date.date() > datetime.today().date():
                print("Future dates are not allowed.")
                continue

            return date_text

        except ValueError:
            print("Invalid date. Example: 2026-10-15")


def get_valid_amount():
    """Accept only a positive numeric amount."""
    while True:
        amount_text = input("Amount (Rs.): ").strip()

        try:
            amount = float(amount_text)

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            if not amount < float("inf"):
                print("Enter a valid finite amount.")
                continue

            return f"{amount:.2f}"

        except ValueError:
            print("Invalid amount. Enter a number, such as 120.50.")


def add_expense():
    """Collect and save a new expense."""
    print("\n=== ADD EXPENSE ===")

    date = get_valid_date()

    print("\nAvailable categories:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("Choose category number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            category = CATEGORIES[int(choice) - 1]
            break

        print("Invalid choice. Please select a listed category.")

    while True:
        description = input("Description: ").strip()
        if description:
            break
        print("Description cannot be empty.")

    amount = get_valid_amount()

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    save_expense(expense)


def display_expenses(expenses):
    """Print expense records in a table."""
    if not expenses:
        print("No expenses found.")
        return

    print("\n" + "-" * 77)
    print(f"{'Date':<13}{'Category':<12}{'Description':<27}{'Amount (Rs.)':>15}")
    print("-" * 77)

    for expense in expenses:
        print(
            f"{expense['date']:<13}"
            f"{expense['category']:<12}"
            f"{expense['description'][:25]:<27}"
            f"{float(expense['amount']):>15.2f}"
        )

    print("-" * 77)
    total = sum(float(e["amount"]) for e in expenses)
    print(f"{'Total:':<52} Rs. {total:.2f}")


def view_all_expenses():
    """Show every saved expense."""
    print("\n=== ALL EXPENSES ===")
    expenses = load_expenses()
    display_expenses(expenses)


def filter_expenses():
    """Filter expenses by category or month."""
    expenses = load_expenses()

    if not expenses:
        print("No expenses available to filter.")
        return

    print("\n=== FILTER EXPENSES ===")
    print("1. Filter by category")
    print("2. Filter by month")
    print("3. Back to main menu")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("\nCategories:")
        for index, category in enumerate(CATEGORIES, start=1):
            print(f"{index}. {category}")

        category_choice = input("Choose category number: ").strip()

        if not category_choice.isdigit():
            print("Invalid category choice.")
            return

        index = int(category_choice)
        if not 1 <= index <= len(CATEGORIES):
            print("Invalid category choice.")
            return

        category = CATEGORIES[index - 1]
        filtered = [
            e for e in expenses
            if e["category"].lower() == category.lower()
        ]

        print(f"\nExpenses in category: {category}")
        display_expenses(filtered)

    elif choice == "2":
        while True:
            month = input("Enter month (YYYY-MM): ").strip()

            try:
                datetime.strptime(month, "%Y-%m")
                break
            except ValueError:
                print("Invalid month. Example: 2026-10")

        filtered = [
            e for e in expenses
            if e["date"].startswith(month)
        ]

        print(f"\nExpenses for {month}")
        display_expenses(filtered)

    elif choice == "3":
        return

    else:
        print("Invalid option.")


def show_summary():
    """Show category totals, grand total, and largest expense."""
    expenses = load_expenses()

    if not expenses:
        print("No expenses available for summary.")
        return

    category_totals = defaultdict(float)

    for expense in expenses:
        try:
            amount = float(expense["amount"])
            category_totals[expense["category"]] += amount
        except (ValueError, KeyError):
            print("Warning: Skipped an invalid CSV record.")

    print("\n=== EXPENSE SUMMARY ===")
    print("-" * 40)
    print(f"{'Category':<20}{'Total (Rs.)':>15}")
    print("-" * 40)

    for category, total in sorted(category_totals.items()):
        print(f"{category:<20}{total:>15.2f}")

    grand_total = sum(category_totals.values())
    biggest_expense = max(
        expenses,
        key=lambda e: float(e["amount"])
    )

    print("-" * 40)
    print(f"{'Grand Total':<20}{grand_total:>15.2f}")
    print("\n=== BIGGEST SINGLE EXPENSE ===")
    print(f"Date       : {biggest_expense['date']}")
    print(f"Category   : {biggest_expense['category']}")
    print(f"Description: {biggest_expense['description']}")
    print(f"Amount     : Rs. {float(biggest_expense['amount']):.2f}")


def main():
    """Run the menu until the user chooses Quit."""
    ensure_file()

    while True:
        print("\n" + "=" * 40)
        print("       PERSONAL EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Expense summary")
        print("5. Quit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Your expenses are saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
