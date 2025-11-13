"""
Basic usage example for the Bank Management System.

This example demonstrates:
- Creating different types of accounts
- Performing deposits and withdrawals
- Viewing account details
- Transaction history
"""

from bank_management import Bank


def main():
    # Create a bank instance
    bank = Bank(name="Python Bank")

    print("=" * 60)
    print("  Bank Management System - Basic Usage Example")
    print("=" * 60)

    # Create different types of accounts
    print("\n1. Creating Accounts...")
    print("-" * 60)

    checking = bank.create_account(
        account_type="checking",
        account_number="CHK12345",
        account_holder="John Doe",
        initial_balance=1000.0,
        overdraft_limit=500.0,
    )
    print(f"Created: {checking}")

    savings = bank.create_account(
        account_type="savings",
        account_number="SAV67890",
        account_holder="Jane Smith",
        initial_balance=5000.0,
        interest_rate=0.03,
    )
    print(f"Created: {savings}")

    business = bank.create_account(
        account_type="business",
        account_number="BUS11111",
        account_holder="Bob Johnson",
        business_name="Tech Solutions Inc.",
        tax_id="12-3456789",
        initial_balance=10000.0,
    )
    print(f"Created: {business}")

    # Perform transactions
    print("\n2. Performing Transactions...")
    print("-" * 60)

    checking.deposit(500.0)
    print(f"After deposit: Balance = ${checking.get_balance():.2f}")

    checking.withdraw(200.0)
    print(f"After withdrawal: Balance = ${checking.get_balance():.2f}")

    savings.deposit(1000.0)
    print(f"Savings after deposit: Balance = ${savings.get_balance():.2f}")

    # Apply interest to savings account
    print("\n3. Applying Interest...")
    print("-" * 60)
    interest = savings.add_interest()
    print(f"Interest earned: ${interest:.2f}")
    print(f"New savings balance: ${savings.get_balance():.2f}")

    # Transfer money between accounts
    print("\n4. Transferring Money...")
    print("-" * 60)
    transfer_amount = 500.0
    print(f"Transferring ${transfer_amount} from checking to savings...")
    bank.transfer("CHK12345", "SAV67890", transfer_amount)
    print(f"Checking balance: ${checking.get_balance():.2f}")
    print(f"Savings balance: ${savings.get_balance():.2f}")

    # View transaction history
    print("\n5. Transaction History (Checking Account)...")
    print("-" * 60)
    transactions = checking.get_transaction_history(limit=5)
    for txn in transactions:
        print(f"  {txn}")

    # List all accounts
    print("\n6. All Accounts...")
    print("-" * 60)
    for account in bank.list_accounts():
        print(f"  • {account}")

    # Bank statistics
    print("\n7. Bank Statistics...")
    print("-" * 60)
    stats = bank.get_statistics()
    print(f"Total Accounts: {stats['total_accounts']}")
    print(f"Total Balance: ${stats['total_balance']:.2f}")
    print("\nAccounts by Type:")
    for acc_type, count in stats['accounts_by_type'].items():
        balance = stats['balance_by_type'][acc_type]
        print(f"  • {acc_type}: {count} account(s), ${balance:.2f}")

    # Save data
    print("\n8. Saving Data...")
    print("-" * 60)
    bank.save()
    print("Data saved successfully!")

    print("\n" + "=" * 60)
    print("  Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
