"""
Command-line interface for the Bank Management System.
"""

import sys
from typing import Optional

from bank_management.bank import Bank
from bank_management.models import SavingsAccount
from bank_management.exceptions import BankingException
from bank_management.logger import logger


class BankCLI:
    """Interactive command-line interface for bank operations."""

    def __init__(self, bank: Optional[Bank] = None):
        self.bank = bank or Bank()
        self.running = False

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * 50)
        print(f"  {self.bank.name} - Banking System")
        print("=" * 50)
        print("1.  Create Account")
        print("2.  View Account Details")
        print("3.  Deposit Money")
        print("4.  Withdraw Money")
        print("5.  Transfer Money")
        print("6.  View Transaction History")
        print("7.  Apply Interest (Savings Accounts)")
        print("8.  List All Accounts")
        print("9.  Bank Statistics")
        print("10. Save Data")
        print("11. Load Data")
        print("0.  Exit")
        print("=" * 50)

    def get_input(self, prompt: str, input_type=str, default=None):
        """
        Get and validate user input.

        Args:
            prompt: Input prompt to display
            input_type: Expected type (str, int, float)
            default: Default value if input is empty

        Returns:
            Validated input value
        """
        while True:
            try:
                user_input = input(prompt).strip()

                if not user_input and default is not None:
                    return default

                if input_type == str:
                    return user_input
                elif input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return input_type(user_input)

            except ValueError:
                print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None

    def create_account(self) -> None:
        """Create a new account."""
        print("\n--- Create New Account ---")
        print("Account Types: 1. Checking  2. Savings  3. Business")

        account_type_map = {
            "1": "checking",
            "2": "savings",
            "3": "business",
        }

        choice = self.get_input("Select account type (1-3): ")
        if choice not in account_type_map:
            print("Invalid account type.")
            return

        account_type = account_type_map[choice]
        account_number = self.get_input("Enter account number: ")
        account_holder = self.get_input("Enter account holder name: ")
        initial_balance = self.get_input("Enter initial balance: ", float, 0.0)

        try:
            kwargs = {"initial_balance": initial_balance}

            # Account-specific parameters
            if account_type == "savings":
                interest_rate = self.get_input(
                    "Enter interest rate (e.g., 0.02 for 2%): ",
                    float,
                    0.02
                )
                kwargs["interest_rate"] = interest_rate

            elif account_type == "business":
                business_name = self.get_input("Enter business name: ")
                tax_id = self.get_input("Enter tax ID: ")
                kwargs["business_name"] = business_name
                kwargs["tax_id"] = tax_id

            account = self.bank.create_account(
                account_type=account_type,
                account_number=account_number,
                account_holder=account_holder,
                **kwargs,
            )

            print(f"\nAccount created successfully!")
            print(account)

        except BankingException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.error(f"Error creating account: {e}")

    def view_account(self) -> None:
        """View account details."""
        print("\n--- View Account Details ---")
        account_number = self.get_input("Enter account number: ")

        try:
            account = self.bank.get_account(account_number)
            print(f"\n{account}")
            print(f"Account Type: {account.get_account_type()}")
            print(f"Created: {account.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        except BankingException as e:
            print(f"Error: {e}")

    def deposit_money(self) -> None:
        """Deposit money to an account."""
        print("\n--- Deposit Money ---")
        account_number = self.get_input("Enter account number: ")
        amount = self.get_input("Enter deposit amount: ", float)

        try:
            account = self.bank.get_account(account_number)
            account.deposit(amount)
            print(f"\nDeposit successful!")
            print(f"New balance: ${account.get_balance():.2f}")

        except BankingException as e:
            print(f"Error: {e}")

    def withdraw_money(self) -> None:
        """Withdraw money from an account."""
        print("\n--- Withdraw Money ---")
        account_number = self.get_input("Enter account number: ")
        amount = self.get_input("Enter withdrawal amount: ", float)

        try:
            account = self.bank.get_account(account_number)
            account.withdraw(amount)
            print(f"\nWithdrawal successful!")
            print(f"New balance: ${account.get_balance():.2f}")

        except BankingException as e:
            print(f"Error: {e}")

    def transfer_money(self) -> None:
        """Transfer money between accounts."""
        print("\n--- Transfer Money ---")
        from_account = self.get_input("Enter source account number: ")
        to_account = self.get_input("Enter destination account number: ")
        amount = self.get_input("Enter transfer amount: ", float)

        try:
            self.bank.transfer(from_account, to_account, amount)
            print(f"\nTransfer successful!")
            print(f"Transferred ${amount:.2f} from {from_account} to {to_account}")

        except BankingException as e:
            print(f"Error: {e}")

    def view_transactions(self) -> None:
        """View transaction history."""
        print("\n--- Transaction History ---")
        account_number = self.get_input("Enter account number: ")
        limit = self.get_input("Number of transactions to show (Enter for all): ", int, None)

        try:
            account = self.bank.get_account(account_number)
            transactions = account.get_transaction_history(limit)

            if not transactions:
                print("No transactions found.")
                return

            print(f"\nTransaction History for {account_number}:")
            print("-" * 70)
            for txn in transactions:
                print(txn)
            print("-" * 70)
            print(f"Total transactions: {len(transactions)}")

        except BankingException as e:
            print(f"Error: {e}")

    def apply_interest(self) -> None:
        """Apply interest to savings accounts."""
        print("\n--- Apply Interest ---")
        account_number = self.get_input("Enter savings account number: ")

        try:
            account = self.bank.get_account(account_number)

            if not isinstance(account, SavingsAccount):
                print("Error: This is not a savings account.")
                return

            interest = account.add_interest()
            print(f"\nInterest applied: ${interest:.2f}")
            print(f"New balance: ${account.get_balance():.2f}")

        except BankingException as e:
            print(f"Error: {e}")

    def list_accounts(self) -> None:
        """List all accounts."""
        print("\n--- All Accounts ---")
        accounts = self.bank.list_accounts()

        if not accounts:
            print("No accounts found.")
            return

        print(f"\nTotal accounts: {len(accounts)}\n")
        for account in accounts:
            print(f"  • {account}")

    def show_statistics(self) -> None:
        """Show bank statistics."""
        print("\n--- Bank Statistics ---")
        stats = self.bank.get_statistics()

        print(f"\n{self.bank.name}")
        print("-" * 50)
        print(f"Total Accounts: {stats['total_accounts']}")
        print(f"Total Balance: ${stats['total_balance']:.2f}")
        print("\nAccounts by Type:")
        for acc_type, count in stats['accounts_by_type'].items():
            balance = stats['balance_by_type'][acc_type]
            print(f"  • {acc_type}: {count} account(s), ${balance:.2f}")

    def save_data(self) -> None:
        """Save bank data."""
        try:
            self.bank.save()
            print("\nData saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self) -> None:
        """Load bank data."""
        try:
            self.bank.load()
            print("\nData loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")

    def run(self) -> None:
        """Run the CLI interface."""
        self.running = True
        print(f"\nWelcome to {self.bank.name}!")

        while self.running:
            try:
                self.display_menu()
                choice = self.get_input("\nEnter your choice: ")

                if choice == "1":
                    self.create_account()
                elif choice == "2":
                    self.view_account()
                elif choice == "3":
                    self.deposit_money()
                elif choice == "4":
                    self.withdraw_money()
                elif choice == "5":
                    self.transfer_money()
                elif choice == "6":
                    self.view_transactions()
                elif choice == "7":
                    self.apply_interest()
                elif choice == "8":
                    self.list_accounts()
                elif choice == "9":
                    self.show_statistics()
                elif choice == "10":
                    self.save_data()
                elif choice == "11":
                    self.load_data()
                elif choice == "0":
                    print("\nThank you for using our banking system. Goodbye!")
                    self.running = False
                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.running = False
            except Exception as e:
                print(f"An error occurred: {e}")
                logger.error(f"CLI error: {e}")


def main():
    """Main entry point for the CLI."""
    cli = BankCLI()
    cli.run()


if __name__ == "__main__":
    main()
