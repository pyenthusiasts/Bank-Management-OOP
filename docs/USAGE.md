# Usage Guide

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Bank-Management-OOP.git
cd Bank-Management-OOP

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Quick Start

```python
from bank_management import Bank

# Create a bank
bank = Bank(name="My Bank")

# Create an account
account = bank.create_account(
    account_type="checking",
    account_number="CHK001",
    account_holder="John Doe",
    initial_balance=1000.0
)

# Perform operations
account.deposit(500.0)
account.withdraw(200.0)

# View balance
print(f"Balance: ${account.get_balance():.2f}")
```

## Using the CLI

The package includes an interactive CLI:

```bash
# Run the CLI
bank-cli

# Or run directly
python -m bank_management.cli
```

### CLI Features

- Create accounts (Checking, Savings, Business)
- Deposit and withdraw money
- Transfer between accounts
- View transaction history
- Apply interest to savings accounts
- Save and load data
- View bank statistics

## Account Types

### 1. Checking Account

Best for everyday transactions.

```python
checking = bank.create_account(
    account_type="checking",
    account_number="CHK001",
    account_holder="John Doe",
    initial_balance=1000.0,
    overdraft_limit=500.0,      # Optional: default 100.0
    transaction_fee=1.0,         # Optional: default 0.0
    free_transactions=5          # Optional: default 5
)
```

**Features:**
- Overdraft protection
- Optional transaction fees (after free transaction limit)
- Unlimited deposits and withdrawals

### 2. Savings Account

Best for saving money with interest.

```python
savings = bank.create_account(
    account_type="savings",
    account_number="SAV001",
    account_holder="Jane Doe",
    initial_balance=5000.0,
    interest_rate=0.03,          # Optional: default 0.02 (2%)
    minimum_balance=500.0,       # Optional: default 100.0
    withdrawal_limit=6           # Optional: default 6
)

# Apply interest
interest = savings.add_interest()
print(f"Interest earned: ${interest:.2f}")
```

**Features:**
- Earns interest
- Minimum balance requirement
- Monthly withdrawal limit
- Higher interest rates for larger balances

### 3. Business Account

Best for business operations.

```python
business = bank.create_account(
    account_type="business",
    account_number="BUS001",
    account_holder="Bob Smith",
    business_name="Tech Corp",
    tax_id="12-3456789",
    initial_balance=10000.0,
    monthly_fee=25.0             # Optional: default 10.0
)

# Charge monthly fee
business.charge_monthly_fee()
```

**Features:**
- Business information tracking
- Monthly maintenance fees
- Unlimited transactions
- Transaction history for accounting

## Common Operations

### Deposits

```python
account.deposit(500.0)
```

### Withdrawals

```python
account.withdraw(200.0)
```

### Transfers

```python
bank.transfer(
    from_account_number="CHK001",
    to_account_number="SAV001",
    amount=1000.0
)
```

### Transaction History

```python
# Get all transactions
history = account.get_transaction_history()

# Get last 10 transactions
recent = account.get_transaction_history(limit=10)

# Print transactions
for txn in history:
    print(txn)
```

## Data Persistence

### Saving Data

```python
# Save all accounts
bank.save()
```

### Loading Data

```python
# Load previously saved accounts
bank.load()
```

### Creating Backups

```python
# Create backup
backup_path = bank.storage.backup()
print(f"Backup saved to: {backup_path}")

# Create backup with custom path
bank.storage.backup("my_backup.json")
```

## Error Handling

```python
from bank_management.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    MinimumBalanceError,
    AccountNotFoundError,
)

try:
    account.withdraw(10000.0)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"Current balance: ${e.balance:.2f}")
    print(f"Attempted withdrawal: ${e.amount:.2f}")

try:
    account.deposit(-100.0)
except InvalidAmountError as e:
    print(f"Error: {e}")

try:
    bank.get_account("NONEXISTENT")
except AccountNotFoundError as e:
    print(f"Error: {e}")
```

## Bank Statistics

```python
stats = bank.get_statistics()

print(f"Total Accounts: {stats['total_accounts']}")
print(f"Total Balance: ${stats['total_balance']:.2f}")

print("\nAccounts by Type:")
for acc_type, count in stats['accounts_by_type'].items():
    balance = stats['balance_by_type'][acc_type]
    print(f"  {acc_type}: {count} accounts, ${balance:.2f}")
```

## Advanced Usage

### Custom Interest Calculation

```python
# Apply interest multiple times (e.g., monthly for a year)
for month in range(12):
    interest = savings.add_interest()
    print(f"Month {month + 1}: Interest ${interest:.2f}")
```

### Batch Operations

```python
# Process multiple transactions
transactions = [
    ("deposit", 100.0),
    ("withdraw", 50.0),
    ("deposit", 200.0),
]

for operation, amount in transactions:
    if operation == "deposit":
        account.deposit(amount)
    elif operation == "withdraw":
        account.withdraw(amount)
```

### Account Lifecycle Management

```python
# Create account
account = bank.create_account("checking", "TMP001", "Temp User")

# Use account
account.deposit(1000.0)

# Delete when no longer needed
bank.delete_account("TMP001")
```

## Best Practices

1. **Always handle exceptions** when performing financial operations
2. **Save data regularly** to persist changes
3. **Use appropriate account types** for different purposes
4. **Validate inputs** before passing to methods
5. **Monitor transaction limits** for savings and checking accounts
6. **Create backups** before major operations
7. **Review transaction history** regularly

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py` - Simple operations and account management
- `advanced_usage.py` - Error handling and complex scenarios

Run examples:

```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```
