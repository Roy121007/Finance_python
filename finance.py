from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Expense:
    name: str
    amount: float


@dataclass
class UserFinance:
    name: str
    monthly_income: float
    expenses: Dict[str, List[Expense]] = field(default_factory=dict)
    saved_money: float = 0.0

    @property
    def total_expenses(self) -> float:
        return sum(
            item.amount
            for cat_list in self.expenses.values()
            for item in cat_list
        )

    @property
    def net_balance(self) -> float:
        return self.monthly_income - self.total_expenses - self.saved_money


class FinanceTrackerApp:
    def __init__(self) -> None:
        self.user: UserFinance | None = None

    @staticmethod
    def _prompt_float(prompt: str, min_val: float = 0.0, max_val: float | None = None) -> float:
        """Helper method to safely get float inputs with validation"""
        while True:
            try:
                val = float(input(prompt))
                if val < min_val:
                    print(f"Amount must be at least {min_val}")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Amount cannot exceed {max_val}")
                    continue
                return val
            except ValueError:
                print("Invalid input please enter a valid numerical value, Thanks")

    @staticmethod
    def _prompt_int(prompt: str, valid_options: range | list) -> int:
        """Helper method to safely get menu option integers."""
        while True:
            try:
                val = int(input(prompt))
                if val not in valid_options:
                    print(f"Option must be one of {list(valid_options)}.")
                    continue
                return val
            except ValueError:
                print("Invalid input, please enter a valid int, Thanks")

    def setup_user(self) -> None:
        name = input("Enter your name: ").strip().title()
        income = self._prompt_float("Enter your monthly income ($): ", min_val=0.0)
        self.user = UserFinance(name=name, monthly_income=income)
        print(f"\nWelcome, {self.user.name}! Your income is set to ${self.user.monthly_income:,.2f}\n")

    def add_expenses(self) -> None:
        count = int(self._prompt_float("How many expenses would you like to add? ", min_val=1))

        for i in range(1, count + 1):
            print(f"\n--- Expense #{i} ---")
            category = input("Enter category (Rent, Food, etc.): ").strip().title() or "Uncategorized"
            name = input("Enter description/name: ").strip().capitalize() or "General"
            amount = self._prompt_float("Enter amount ($): ", min_val=0.01)

            expense_item = Expense(name=name, amount=amount)
            self.user.expenses.setdefault(category, []).append(expense_item)
            print(f"Added: [{category}] {name} - ${amount:,.2f}")

    def manage_savings(self) -> None:
        print("\n--- Savings Configuration ---")
        print("1. Set percentage of monthly income")
        print("2. Set fixed dollar amount")
        choice = self._prompt_int("Select option (1-2): ", valid_options=[1, 2])

        if choice == 1:
            pct = self._prompt_float("Enter savings percentage (0-100%): ", min_val=0.0, max_val=100.0)
            self.user.saved_money = self.user.monthly_income * (pct / 100.0)
        else:
            self.user.saved_money = self.prompt_float(
                "Enter savings amount ($): ",
                min_val=0.0,
                max_val=self.user.monthly_income
            )

        print(f"Saved amount updated to: ${self.user.saved_money:,.2f}")

    def display_balance(self) -> None:
        print("\n" + "=" * 35)
        print(f"\t  FINANCIAL SUMMARY FOR {self.user.name.upper()}")
        print("=" * 35)
        print(f"Monthly Income:   ${self.user.monthly_income:,.2f}")
        print(f"Total Savings:    ${self.user.saved_money:,.2f}")
        print(f"Total Expenses:   ${self.user.total_expenses:,.2f}")
        print("-" * 35)

        if self.user.expenses:
            print("\nExpense Breakdown by Category:")
            for category, items in self.user.expenses.items():
                cat_total = sum(i.amount for i in items)
                print(f"  • {category}: ${cat_total:,.2f}")
                for item in items:
                    print(f"     - {item.name}: ${item.amount:,.2f}")
        else:
            print("\nNo expenses recorded yet.")

        print("-" * 35)
        print(f"Remaining Balance: ${self.user.net_balance:,.2f}")
        print("=" * 35 + "\n")

    def run(self) -> None:
        self.setup_user()

        menu = (
            "\n===== MENU =====\n"
            "1. Add Expenses\n"
            "2. Set Savings Target\n"
            "3. View Financial Summary\n"
            "4. Exit\n"
        )

        while True:
            print(menu)
            choice = self._prompt_int("Select an option (1-4): ", valid_options=range(1, 5))

            if choice == 1:
                self.add_expenses()
            elif choice == 2:
                self.manage_savings()
            elif choice == 3:
                self.display_balance()
            elif choice == 4:
                print(f"\nThank you, {self.user.name}. Have a great day!")
                break


if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.run()