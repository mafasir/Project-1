import json
import os
from datetime import datetime

DATA_FILE = 'expenses.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"transactions": [], "budgets": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_transaction(data, type_, amount, category, date=None):
    transaction = {
        "type": type_,
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data["transactions"].append(transaction)
    save_data(data)
    print("Transaction added successfully.")

def set_budget(data, category, amount):
    data["budgets"][category] = amount
    save_data(data)
    print(f"Budget for '{category}' set to {amount}.")

def view_transactions(data):
    print("\nTransaction History:")
    for t in data["transactions"]:
        print(f"{t['date']} - {t['type']} - {t['category']} - ${t['amount']}")

def view_budget(data):
    print("\nBudget Report:")
    spent = {}
    for t in data["transactions"]:
        if t["type"] == "expense":
            spent[t["category"]] = spent.get(t["category"], 0) + t["amount"]
    for category, budget in data["budgets"].items():
        used = spent.get(category, 0)
        remaining = budget - used
        print(f"{category}: Budget: ${budget}, Spent: ${used}, Remaining: ${remaining}")

def main():
    data = load_data()
    while True:
        print("\nCommands: add, budget, history, report, exit")
        cmd = input("Enter command: ").lower()

        if cmd == "add":
            type_ = input("Type (income/expense): ").strip().lower()
            amount = float(input("Amount: "))
            category = input("Category: ").strip()
            add_transaction(data, type_, amount, category)

        elif cmd == "budget":
            category = input("Category to set budget for: ").strip()
            amount = float(input("Budget amount: "))
            set_budget(data, category, amount)

        elif cmd == "history":
            view_transactions(data)

        elif cmd == "report":
            view_budget(data)

        elif cmd == "exit":
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
