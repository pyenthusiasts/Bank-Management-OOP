# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-11-13

### Added
- **Complete project reorganization** with modular architecture
- **New account type**: BusinessAccount with monthly fees and business information
- **Data persistence** layer with JSON storage
- **Comprehensive logging** system throughout the application
- **Interactive CLI** interface for easy user interaction
- **Transaction tracking** system with detailed history
- **Type hints** throughout the codebase
- **Custom exceptions** for better error handling:
  - InsufficientFundsError
  - InvalidAmountError
  - AccountNotFoundError
  - AccountAlreadyExistsError
  - MinimumBalanceError
- **Bank management** class for handling multiple accounts
- **Storage features**:
  - Save/load functionality
  - Automatic backups
  - Metadata tracking
- **Enhanced account features**:
  - Overdraft protection for checking accounts
  - Transaction fees with free transaction limits
  - Minimum balance requirements for savings
  - Monthly withdrawal limits
  - Interest calculation
- **Comprehensive test suite** with pytest:
  - Unit tests for all modules
  - 90%+ code coverage
  - Integration tests
- **GitHub Actions** CI/CD workflows:
  - Automated testing on multiple Python versions
  - Code quality checks (flake8, black, isort, mypy)
  - Security scanning
- **Complete documentation**:
  - API reference
  - Usage guide
  - Contributing guidelines
- **Example scripts**:
  - Basic usage example
  - Advanced usage with error handling
- **Professional project structure**:
  - Modular package organization
  - Separate tests directory
  - Examples and documentation folders

### Changed
- **Refactored** single-file implementation into modular package
- **Enhanced** account models with additional features and validation
- **Improved** error messages and exception handling
- **Updated** README with comprehensive documentation and badges
- **Reorganized** code following industry best practices

### Technical Improvements
- Added abstract base classes for better OOP design
- Implemented design patterns (Abstract Factory, Strategy, Repository, Command)
- Added transaction history tracking for all operations
- Improved encapsulation with protected attributes
- Enhanced polymorphism with method overriding
- Added comprehensive docstrings throughout
- Improved code organization and separation of concerns

## [1.0.0] - Previous

### Initial Release
- Basic BankAccount abstract class
- CheckingAccount implementation
- SavingsAccount with interest calculation
- Simple deposit and withdrawal operations
- Basic exception handling
- Console output for operations
- Single-file implementation

---

[2.0.0]: https://github.com/pyenthusiasts/Bank-Management-OOP/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/pyenthusiasts/Bank-Management-OOP/releases/tag/v1.0.0
