# Bank Management System - OOP Implementation

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI](https://github.com/pyenthusiasts/Bank-Management-OOP/workflows/CI/badge.svg)](https://github.com/pyenthusiasts/Bank-Management-OOP/actions)

A comprehensive, production-ready bank management system demonstrating advanced Object-Oriented Programming (OOP) principles in Python. This project showcases inheritance, polymorphism, encapsulation, abstraction, exception handling, and professional software development practices.

## Features

- **Multiple Account Types**
  - Checking Account with overdraft protection
  - Savings Account with interest calculation
  - Business Account with monthly fees

- **Core Banking Operations**
  - Deposits and withdrawals
  - Inter-account transfers
  - Transaction history tracking
  - Balance inquiries

- **Advanced Features**
  - Data persistence with JSON storage
  - Comprehensive logging system
  - Interactive CLI interface
  - Type hints throughout
  - Extensive error handling
  - Unit test coverage

- **OOP Principles Demonstrated**
  - Abstraction (Abstract Base Classes)
  - Encapsulation (Protected attributes)
  - Inheritance (Account type hierarchy)
  - Polymorphism (Method overriding)
  - Exception handling (Custom exceptions)

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [CLI Interface](#cli-interface)
- [Documentation](#documentation)
- [Examples](#examples)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7 or higher

### Install from Source

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Bank-Management-OOP.git
cd Bank-Management-OOP

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Install from PyPI (Coming Soon)

```bash
pip install bank-management-oop
```

## Quick Start

### Using the Python API

```python
from bank_management import Bank

# Create a bank instance
bank = Bank(name="Python Bank")

# Create a checking account
checking = bank.create_account(
    account_type="checking",
    account_number="CHK12345",
    account_holder="John Doe",
    initial_balance=1000.0
)

# Perform operations
checking.deposit(500.0)
checking.withdraw(200.0)

# Check balance
print(f"Balance: ${checking.get_balance():.2f}")  # Balance: $1300.00

# View transaction history
for transaction in checking.get_transaction_history():
    print(transaction)
```

### Using the CLI

```bash
# Launch the interactive CLI
bank-cli

# Or run directly with Python
python -m bank_management.cli
```

## Usage

### Account Types

#### Checking Account

```python
checking = bank.create_account(
    account_type="checking",
    account_number="CHK001",
    account_holder="John Doe",
    initial_balance=1000.0,
    overdraft_limit=500.0,      # Overdraft protection
    transaction_fee=1.0,         # Fee after free transactions
    free_transactions=5          # Free transactions per month
)
```

#### Savings Account

```python
savings = bank.create_account(
    account_type="savings",
    account_number="SAV001",
    account_holder="Jane Smith",
    initial_balance=5000.0,
    interest_rate=0.03,          # 3% annual interest
    minimum_balance=500.0,       # Minimum balance requirement
    withdrawal_limit=6           # Monthly withdrawal limit
)

# Apply interest
interest = savings.add_interest()
print(f"Interest earned: ${interest:.2f}")
```

#### Business Account

```python
business = bank.create_account(
    account_type="business",
    account_number="BUS001",
    account_holder="Bob Johnson",
    business_name="Tech Solutions Inc.",
    tax_id="12-3456789",
    initial_balance=10000.0,
    monthly_fee=25.0             # Monthly maintenance fee
)
```

### Transfers

```python
# Transfer money between accounts
bank.transfer(
    from_account_number="CHK001",
    to_account_number="SAV001",
    amount=500.0
)
```

### Data Persistence

```python
# Save all accounts to disk
bank.save()

# Load accounts from disk
bank.load()

# Create backup
backup_path = bank.storage.backup()
print(f"Backup created: {backup_path}")
```

### Error Handling

```python
from bank_management.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    AccountNotFoundError
)

try:
    account.withdraw(10000.0)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"Available balance: ${e.balance:.2f}")
```

## CLI Interface

The system includes a full-featured interactive command-line interface:

```
==================================================
  Python Bank - Banking System
==================================================
1.  Create Account
2.  View Account Details
3.  Deposit Money
4.  Withdraw Money
5.  Transfer Money
6.  View Transaction History
7.  Apply Interest (Savings Accounts)
8.  List All Accounts
9.  Bank Statistics
10. Save Data
11. Load Data
0.  Exit
==================================================
```

## Documentation

Comprehensive documentation is available:

- **[API Reference](docs/API.md)** - Complete API documentation
- **[Usage Guide](docs/USAGE.md)** - Detailed usage instructions
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute

## Examples

The `examples/` directory contains working examples:

### Basic Usage

```bash
python examples/basic_usage.py
```

Demonstrates:
- Creating different account types
- Performing deposits and withdrawals
- Viewing transaction history
- Bank statistics

### Advanced Usage

```bash
python examples/advanced_usage.py
```

Demonstrates:
- Error handling
- Account constraints
- Complex transfers
- Data persistence

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=bank_management --cov-report=html
```

### Run Specific Tests

```bash
# Test specific module
pytest tests/test_models.py

# Test specific class
pytest tests/test_models.py::TestCheckingAccount

# Test specific method
pytest tests/test_models.py::TestCheckingAccount::test_deposit
```

## Project Structure

```
Bank-Management-OOP/
├── bank_management/           # Main package
│   ├── __init__.py           # Package initialization
│   ├── models.py             # Account models
│   ├── bank.py               # Bank management class
│   ├── exceptions.py         # Custom exceptions
│   ├── storage.py            # Data persistence
│   ├── logger.py             # Logging configuration
│   └── cli.py                # CLI interface
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_bank.py
│   ├── test_storage.py
│   └── test_exceptions.py
├── examples/                  # Example scripts
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/                      # Documentation
│   ├── API.md
│   ├── USAGE.md
│   └── CONTRIBUTING.md
├── .github/                   # GitHub workflows
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
├── requirements-dev.txt       # Dev dependencies
├── pytest.ini                 # Pytest configuration
├── .gitignore                # Git ignore rules
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Architecture

### Class Hierarchy

```
BankAccount (ABC)
├── CheckingAccount
├── SavingsAccount
└── BusinessAccount

Bank
└── manages multiple BankAccount instances

BankStorage
└── handles data persistence

Transaction
└── tracks individual transactions
```

### Key Design Patterns

- **Abstract Factory**: Account creation through Bank class
- **Strategy Pattern**: Different account behaviors
- **Repository Pattern**: Data persistence layer
- **Command Pattern**: Transaction tracking

## Requirements

### Runtime Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

### Development Requirements

- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- black >= 22.0.0
- flake8 >= 5.0.0
- mypy >= 0.990
- isort >= 5.10.0

## Contributing

Contributions are welcome! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/pyenthusiasts/Bank-Management-OOP.git
cd Bank-Management-OOP

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black bank_management tests

# Sort imports
isort bank_management tests

# Lint
flake8 bank_management

# Type check
mypy bank_management
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built as an educational demonstration of OOP principles
- Inspired by real-world banking systems
- Designed for learning and teaching Python

## Support

- **Issues**: [GitHub Issues](https://github.com/pyenthusiasts/Bank-Management-OOP/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pyenthusiasts/Bank-Management-OOP/discussions)
- **Documentation**: [docs/](docs/)

## Roadmap

- [ ] Web interface with Flask/FastAPI
- [ ] Database integration (SQLite, PostgreSQL)
- [ ] Multi-currency support
- [ ] Account statements and reports
- [ ] Additional account types (Credit, Loan)
- [ ] Authentication and authorization
- [ ] API endpoints (REST/GraphQL)
- [ ] Mobile app integration

## Statistics

- **Lines of Code**: ~2000+
- **Test Coverage**: 90%+
- **Documentation**: Comprehensive
- **Examples**: Multiple working examples

---

Made with dedication by the Bank Management Team

**Star this repository if you find it useful!**
