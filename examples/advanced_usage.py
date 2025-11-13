"""
Advanced usage example demonstrating error handling and edge cases.
"""

from bank_management import Bank
from bank_management.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    MinimumBalanceError,
    AccountNotFoundError,
)


def main():
    bank = Bank(name="Advanced Bank Demo")

    print("=" * 60)
    print("  Advanced Features & Error Handling Demo")
    print("=" * 60)

    # 1. Demonstrate error handling
    print("\n1. Error Handling Examples...")
    print("-" * 60)

    account = bank.create_account(
        "checking",
        "CHK001",
        "Test User",
        initial_balance=500.0,
        overdraft_limit=100.0,
    )

    # Invalid deposit
    try:
        account.deposit(-50.0)
    except InvalidAmountError as e:
        print(f"Invalid deposit caught: {e}")

    # Insufficient funds
    try:
        account.withdraw(700.0)  # Exceeds balance + overdraft
    except InsufficientFundsError as e:
        print(f"Insufficient funds caught: {e}")

    # Account not found
    try:
        bank.get_account("NONEXISTENT")
    except AccountNotFoundError as e:
        print(f"Account not found: {e}")

    # 2. Savings account constraints
    print("\n2. Savings Account Constraints...")
    print("-" * 60)

    savings = bank.create_account(
        "savings",
        "SAV001",
        "Jane Doe",
        initial_balance=1000.0,
        minimum_balance=500.0,
        withdrawal_limit=3,
    )

    # Attempt to violate minimum balance
    try:
        savings.withdraw(600.0)  # Would leave balance below minimum
    except MinimumBalanceError as e:
        print(f"Minimum balance violation: {e}")

    # Exceed withdrawal limit
    print(f"\nMaking {savings.withdrawal_limit} withdrawals...")
    for i in range(savings.withdrawal_limit):
        savings.withdraw(50.0)
        print(f"  Withdrawal {i+1} successful")

    try:
        savings.withdraw(50.0)  # Should fail - limit exceeded
    except Exception as e:
        print(f"Withdrawal limit exceeded: {e}")

    # 3. Business account features
    print("\n3. Business Account Features...")
    print("-" * 60)

    business = bank.create_account(
        "business",
        "BUS001",
        "John Smith",
        business_name="Acme Corp",
        tax_id="98-7654321",
        initial_balance=5000.0,
        monthly_fee=25.0,
    )

    print(f"Initial balance: ${business.get_balance():.2f}")
    business.charge_monthly_fee()
    print(f"After monthly fee: ${business.get_balance():.2f}")

    # 4. Account lifecycle
    print("\n4. Account Lifecycle...")
    print("-" * 60)

    temp_account = bank.create_account(
        "checking",
        "TEMP001",
        "Temp User",
        initial_balance=100.0,
    )
    print(f"Created temporary account: {temp_account.account_number}")

    print(f"Total accounts before deletion: {len(bank.list_accounts())}")
    bank.delete_account("TEMP001")
    print(f"Total accounts after deletion: {len(bank.list_accounts())}")

    # 5. Complex transfers
    print("\n5. Complex Transfer Scenario...")
    print("-" * 60)

    acc1 = bank.create_account("checking", "ACC1", "User A", initial_balance=1000.0)
    acc2 = bank.create_account("checking", "ACC2", "User B", initial_balance=500.0)
    acc3 = bank.create_account("savings", "ACC3", "User C", initial_balance=2000.0, minimum_balance=0.0)

    print("Initial balances:")
    print(f"  ACC1: ${acc1.get_balance():.2f}")
    print(f"  ACC2: ${acc2.get_balance():.2f}")
    print(f"  ACC3: ${acc3.get_balance():.2f}")

    # Chain of transfers
    bank.transfer("ACC1", "ACC2", 200.0)
    bank.transfer("ACC2", "ACC3", 300.0)
    bank.transfer("ACC3", "ACC1", 150.0)

    print("\nFinal balances after transfers:")
    print(f"  ACC1: ${acc1.get_balance():.2f}")
    print(f"  ACC2: ${acc2.get_balance():.2f}")
    print(f"  ACC3: ${acc3.get_balance():.2f}")

    # 6. Detailed transaction history
    print("\n6. Detailed Transaction History (ACC1)...")
    print("-" * 60)
    for txn in acc1.get_transaction_history():
        print(f"  {txn}")

    # 7. Persistence
    print("\n7. Data Persistence...")
    print("-" * 60)
    bank.save()
    print("Data saved to: bank_data.json")

    # Create backup
    backup_path = bank.storage.backup()
    print(f"Backup created at: {backup_path}")

    print("\n" + "=" * 60)
    print("  Advanced demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
