#!/usr/bin/env python3
"""
Quick demo script for Bank Management System.
Run this to see the system in action!
"""

from bank_management import Bank
from bank_management.exceptions import BankingException


def main():
    print("=" * 70)
    print("  BANK MANAGEMENT SYSTEM - QUICK DEMO")
    print("=" * 70)

    # Create bank
    bank = Bank(name="Demo Bank")
    print(f"\n✓ Created '{bank.name}'\n")

    # Create accounts
    print("Creating accounts...")

    checking = bank.create_account(
        "checking",
        "CHK001",
        "Alice Johnson",
        initial_balance=2000.0,
        overdraft_limit=500.0
    )
    print(f"  ✓ {checking}")

    savings = bank.create_account(
        "savings",
        "SAV001",
        "Bob Smith",
        initial_balance=10000.0,
        interest_rate=0.04
    )
    print(f"  ✓ {savings}")

    business = bank.create_account(
        "business",
        "BUS001",
        "Charlie Brown",
        business_name="Tech Innovators LLC",
        tax_id="12-3456789",
        initial_balance=50000.0
    )
    print(f"  ✓ {business}")

    # Perform operations
    print("\n" + "-" * 70)
    print("Performing transactions...")
    print("-" * 70)

    print("\n1. Depositing $500 to checking account...")
    checking.deposit(500.0)
    print(f"   New balance: ${checking.get_balance():,.2f}")

    print("\n2. Withdrawing $300 from checking account...")
    checking.withdraw(300.0)
    print(f"   New balance: ${checking.get_balance():,.2f}")

    print("\n3. Transferring $1,000 from checking to savings...")
    bank.transfer("CHK001", "SAV001", 1000.0)
    print(f"   Checking balance: ${checking.get_balance():,.2f}")
    print(f"   Savings balance: ${savings.get_balance():,.2f}")

    print("\n4. Applying interest to savings account...")
    interest = savings.add_interest()
    print(f"   Interest earned: ${interest:,.2f}")
    print(f"   New balance: ${savings.get_balance():,.2f}")

    print("\n5. Charging monthly fee on business account...")
    business.charge_monthly_fee()
    print(f"   New balance: ${business.get_balance():,.2f}")

    # Show statistics
    print("\n" + "=" * 70)
    print("BANK STATISTICS")
    print("=" * 70)
    stats = bank.get_statistics()
    print(f"Total Accounts: {stats['total_accounts']}")
    print(f"Total Assets: ${stats['total_balance']:,.2f}")
    print("\nBreakdown by Account Type:")
    for acc_type, count in stats['accounts_by_type'].items():
        balance = stats['balance_by_type'][acc_type]
        print(f"  • {acc_type}: {count} account(s) - ${balance:,.2f}")

    # Show recent transactions
    print("\n" + "=" * 70)
    print("RECENT TRANSACTIONS (Checking Account)")
    print("=" * 70)
    for txn in checking.get_transaction_history(limit=5):
        print(f"  {txn}")

    # Demonstrate error handling
    print("\n" + "=" * 70)
    print("DEMONSTRATING ERROR HANDLING")
    print("=" * 70)

    print("\nAttempting to withdraw more than available balance...")
    try:
        checking.withdraw(50000.0)
    except BankingException as e:
        print(f"  ✗ Error caught: {e}")

    print("\nAttempting to deposit negative amount...")
    try:
        checking.deposit(-100.0)
    except BankingException as e:
        print(f"  ✗ Error caught: {e}")

    # Save data
    print("\n" + "=" * 70)
    print("DATA PERSISTENCE")
    print("=" * 70)
    bank.save()
    print("✓ Bank data saved to 'bank_data.json'")

    backup = bank.storage.backup()
    print(f"✓ Backup created: {backup}")

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  • Run 'python -m bank_management.cli' for interactive mode")
    print("  • Check 'examples/' for more usage examples")
    print("  • Read 'docs/USAGE.md' for detailed documentation")
    print("\n")


if __name__ == "__main__":
    main()
