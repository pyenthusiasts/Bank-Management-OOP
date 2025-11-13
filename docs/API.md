# API Documentation

## Table of Contents

- [Bank Class](#bank-class)
- [Account Classes](#account-classes)
  - [BankAccount (Abstract)](#bankaccount-abstract)
  - [CheckingAccount](#checkingaccount)
  - [SavingsAccount](#savingsaccount)
  - [BusinessAccount](#businessaccount)
- [Exceptions](#exceptions)
- [Storage](#storage)

## Bank Class

The main class for managing multiple bank accounts.

### Constructor

```python
Bank(name: str = "Python Bank", storage_path: str = "bank_data.json")
```

**Parameters:**
- `name`: Name of the bank
- `storage_path`: Path to the data storage file

### Methods

#### `create_account(account_type, account_number, account_holder, **kwargs)`

Create a new bank account.

**Parameters:**
- `account_type`: Type of account ("checking", "savings", "business")
- `account_number`: Unique account identifier
- `account_holder`: Name of the account holder
- `**kwargs`: Account-specific parameters

**Returns:** BankAccount instance

**Raises:** AccountAlreadyExistsError, ValueError

**Example:**
```python
bank = Bank()
account = bank.create_account(
    account_type="checking",
    account_number="CHK001",
    account_holder="John Doe",
    initial_balance=1000.0
)
```

#### `get_account(account_number)`

Retrieve an account by its number.

**Parameters:**
- `account_number`: Account identifier

**Returns:** BankAccount instance

**Raises:** AccountNotFoundError

#### `delete_account(account_number)`

Delete an account.

**Parameters:**
- `account_number`: Account identifier

**Raises:** AccountNotFoundError

#### `list_accounts()`

Get a list of all accounts.

**Returns:** List[BankAccount]

#### `get_total_balance()`

Calculate total balance across all accounts.

**Returns:** float

#### `transfer(from_account_number, to_account_number, amount)`

Transfer money between accounts.

**Parameters:**
- `from_account_number`: Source account
- `to_account_number`: Destination account
- `amount`: Amount to transfer

**Raises:** AccountNotFoundError, InsufficientFundsError, InvalidAmountError

#### `save()`

Save all accounts to persistent storage.

#### `load()`

Load accounts from persistent storage.

#### `get_statistics()`

Get bank statistics.

**Returns:** Dictionary containing:
- `total_accounts`: Total number of accounts
- `total_balance`: Total balance
- `accounts_by_type`: Count by account type
- `balance_by_type`: Total balance by type

---

## Account Classes

### BankAccount (Abstract)

Abstract base class for all account types.

#### Constructor

```python
BankAccount(account_number: str, account_holder: str, initial_balance: float = 0.0)
```

#### Methods

##### `deposit(amount)` (Abstract)

Deposit money into the account.

##### `withdraw(amount)` (Abstract)

Withdraw money from the account.

##### `get_balance()`

Get the current balance.

**Returns:** float

##### `get_transaction_history(limit=None)`

Get transaction history.

**Parameters:**
- `limit`: Optional limit on number of transactions

**Returns:** List[Transaction]

##### `get_account_type()`

Get the account type name.

**Returns:** str

##### `to_dict()`

Convert account to dictionary.

**Returns:** dict

---

### CheckingAccount

Checking account with overdraft protection and transaction fees.

#### Constructor

```python
CheckingAccount(
    account_number: str,
    account_holder: str,
    initial_balance: float = 0.0,
    overdraft_limit: float = 100.0,
    transaction_fee: float = 0.0,
    free_transactions: int = 5
)
```

**Parameters:**
- `account_number`: Unique identifier
- `account_holder`: Account holder name
- `initial_balance`: Starting balance
- `overdraft_limit`: Maximum negative balance allowed
- `transaction_fee`: Fee per transaction (after free transactions)
- `free_transactions`: Number of free transactions per month

#### Methods

##### `deposit(amount)`

Deposit money. May incur transaction fee.

##### `withdraw(amount)`

Withdraw money. Allows overdraft up to limit.

##### `reset_monthly_transactions()`

Reset the monthly transaction counter.

---

### SavingsAccount

Savings account with interest and withdrawal limits.

#### Constructor

```python
SavingsAccount(
    account_number: str,
    account_holder: str,
    initial_balance: float = 0.0,
    interest_rate: float = 0.02,
    minimum_balance: float = 100.0,
    withdrawal_limit: int = 6
)
```

**Parameters:**
- `account_number`: Unique identifier
- `account_holder`: Account holder name
- `initial_balance`: Starting balance
- `interest_rate`: Annual interest rate (as decimal)
- `minimum_balance`: Minimum required balance
- `withdrawal_limit`: Maximum withdrawals per month

#### Methods

##### `deposit(amount)`

Deposit money into savings.

##### `withdraw(amount)`

Withdraw money. Enforces minimum balance and withdrawal limit.

**Raises:** MinimumBalanceError, BankingException

##### `add_interest()`

Calculate and add interest to balance.

**Returns:** float (interest amount)

##### `reset_monthly_withdrawals()`

Reset the monthly withdrawal counter.

---

### BusinessAccount

Business account with monthly fees.

#### Constructor

```python
BusinessAccount(
    account_number: str,
    account_holder: str,
    business_name: str,
    tax_id: str,
    initial_balance: float = 0.0,
    monthly_fee: float = 10.0
)
```

**Parameters:**
- `account_number`: Unique identifier
- `account_holder`: Account holder name
- `business_name`: Name of the business
- `tax_id`: Tax identification number
- `initial_balance`: Starting balance
- `monthly_fee`: Monthly maintenance fee

#### Methods

##### `deposit(amount)`

Deposit money into business account.

##### `withdraw(amount)`

Withdraw money from business account.

##### `charge_monthly_fee()`

Charge the monthly maintenance fee.

---

## Exceptions

### BankingException

Base exception for all banking errors.

### InsufficientFundsError

Raised when withdrawal exceeds available funds.

**Attributes:**
- `balance`: Current balance
- `amount`: Attempted withdrawal amount

### InvalidAmountError

Raised for invalid transaction amounts.

**Attributes:**
- `amount`: The invalid amount

### AccountNotFoundError

Raised when account doesn't exist.

**Attributes:**
- `account_number`: The account number

### AccountAlreadyExistsError

Raised when creating duplicate account.

**Attributes:**
- `account_number`: The account number

### MinimumBalanceError

Raised when balance falls below minimum.

**Attributes:**
- `balance`: Current/resulting balance
- `minimum`: Minimum required balance

---

## Storage

### BankStorage

Handles data persistence.

#### Constructor

```python
BankStorage(storage_path: str = "bank_data.json")
```

#### Methods

##### `save(data)`

Save data to JSON file.

**Parameters:**
- `data`: Dictionary to save

##### `load()`

Load data from JSON file.

**Returns:** dict or None

##### `delete()`

Delete the storage file.

##### `backup(backup_path=None)`

Create a backup of the storage file.

**Parameters:**
- `backup_path`: Optional custom backup path

**Returns:** Path to backup file
