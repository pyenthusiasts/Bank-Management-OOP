# Deployment Guide

This guide covers various deployment options for the Bank Management System.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [Traditional Deployment](#traditional-deployment)
- [Development Deployment](#development-deployment)
- [Production Considerations](#production-considerations)

## Docker Deployment

### Building the Image

```bash
# Build the Docker image
docker build -t bank-management-oop:latest .

# Or use docker-compose
docker-compose build
```

### Running with Docker

```bash
# Run the CLI interface
docker run -it bank-management-oop:latest

# Run the demo
docker-compose run demo

# Run tests
docker-compose run test
```

### Docker Compose Services

The `docker-compose.yml` file defines three services:

1. **bank-management**: Interactive CLI
2. **demo**: Runs the demo script
3. **test**: Runs the test suite

```bash
# Start the main service
docker-compose up bank-management

# Run the demo
docker-compose run demo

# Run tests
docker-compose run test
```

### Volume Mounts

To persist data, mount the data directory:

```bash
docker run -it \
  -v $(pwd)/bank_data.json:/app/bank_data.json \
  bank-management-oop:latest
```

## Traditional Deployment

### Requirements

- Python 3.7+
- pip
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/pyenthusiasts/Bank-Management-OOP.git
   cd Bank-Management-OOP
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**
   ```bash
   pip install -e .
   ```

4. **Verify installation**
   ```bash
   bank-cli --help
   python demo.py
   ```

## Development Deployment

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/pyenthusiasts/Bank-Management-OOP.git
cd Bank-Management-OOP

# Install with dev dependencies
make install-dev

# Or manually
pip install -e ".[dev]"
```

### Using Makefile Commands

```bash
# View available commands
make help

# Run tests
make test

# Run with coverage
make test-coverage

# Format code
make format

# Run all checks
make all-checks
```

### Using Tox

For multi-version testing:

```bash
# Install tox
pip install tox

# Run tests on all Python versions
tox

# Run specific environment
tox -e py39

# Run linting
tox -e lint

# Run type checking
tox -e type
```

## Production Considerations

### Security

1. **Data Encryption**
   - Encrypt `bank_data.json` at rest
   - Use environment variables for sensitive config
   - Implement access controls

2. **Authentication**
   - Add user authentication layer
   - Implement role-based access control
   - Use secure session management

3. **Networking**
   - Use HTTPS for all communications
   - Implement rate limiting
   - Add DDoS protection

### Performance

1. **Database**
   - Consider using PostgreSQL or MySQL for production
   - Implement connection pooling
   - Add caching layer (Redis)

2. **Scaling**
   - Use load balancer for multiple instances
   - Implement horizontal scaling
   - Add monitoring and logging

### Monitoring

1. **Logging**
   ```python
   from bank_management.logger import setup_logger

   logger = setup_logger(
       name="bank_production",
       level=logging.INFO,
       log_file="/var/log/bank_management/app.log"
   )
   ```

2. **Health Checks**
   - Implement health check endpoints
   - Monitor system resources
   - Set up alerts for critical errors

### Backup Strategy

1. **Automated Backups**
   ```bash
   # Create daily backups
   0 2 * * * python -c "from bank_management import Bank; Bank().storage.backup()"
   ```

2. **Backup Retention**
   - Keep daily backups for 7 days
   - Keep weekly backups for 4 weeks
   - Keep monthly backups for 1 year

3. **Disaster Recovery**
   - Store backups in multiple locations
   - Test restore procedures regularly
   - Document recovery steps

## Environment Variables

Create a `.env` file (not committed to git):

```bash
# Application settings
BANK_NAME="Production Bank"
STORAGE_PATH="/var/lib/bank_management/bank_data.json"

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/bank_management/app.log

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
```

## Systemd Service (Linux)

Create `/etc/systemd/system/bank-management.service`:

```ini
[Unit]
Description=Bank Management System
After=network.target

[Service]
Type=simple
User=bankuser
WorkingDirectory=/opt/bank-management
ExecStart=/opt/bank-management/venv/bin/python -m bank_management.cli
Restart=always
RestartSec=10

Environment="PYTHONUNBUFFERED=1"
Environment="STORAGE_PATH=/var/lib/bank_management/bank_data.json"

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bank-management
sudo systemctl start bank-management
```

## Web Service Integration

For web service deployment (future enhancement):

```python
# Using Flask
from flask import Flask
from bank_management import Bank

app = Flask(__name__)
bank = Bank()

@app.route('/api/accounts', methods=['GET'])
def list_accounts():
    return jsonify([acc.to_dict() for acc in bank.list_accounts()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

## Cloud Deployment

### AWS

- Use EC2 for compute
- RDS for database
- S3 for backup storage
- CloudWatch for monitoring

### Google Cloud

- Use Compute Engine
- Cloud SQL for database
- Cloud Storage for backups
- Cloud Logging

### Azure

- Use Virtual Machines
- Azure Database
- Blob Storage for backups
- Application Insights

## Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   pip install -e .
   ```

2. **Permission errors on data files**
   ```bash
   chmod 600 bank_data.json
   chown bankuser:bankuser bank_data.json
   ```

3. **Port already in use**
   ```bash
   lsof -i :8000
   kill -9 <PID>
   ```

## Support

For deployment issues:
- Check logs: `tail -f /var/log/bank_management/app.log`
- Run diagnostics: `python -m bank_management --version`
- Report issues: [GitHub Issues](https://github.com/pyenthusiasts/Bank-Management-OOP/issues)
