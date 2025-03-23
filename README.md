# Docker Service Manager

A powerful cross-platform tool for managing Docker services, containers, and images with an interactive interface and health monitoring capabilities.

## Author
Cosmic Soul

## Features

### 1. Service Management
- Start/Stop Docker service
- Check service status
- Enable/Disable service autostart
- Restart service
- Monitor service health

### 2. Container Management
- List running containers
- List all containers (including stopped)
- Remove specific containers
- Prune stopped containers
- View container logs

### 3. Image Management
- List all Docker images
- Remove specific images
- Prune dangling images
- View image details

### 4. System Information
- View Docker system information
- Check resource usage
- Monitor system metrics
- View Docker daemon status

### 5. Health Reports
- Generate comprehensive health reports
- Monitor system resources
- Track Docker metrics
- View performance statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/docker-service-manager.git
cd docker-service-manager
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Basic Usage
```bash
dsm
```

### Run with Options
```bash
dsm --interactive  # Run in interactive mode (default)
dsm --demo        # Run in demo mode
dsm --help        # Show help message
dsm --version     # Show version information
```

### Running with Administrative Privileges
For full functionality, run with sudo:
```bash
sudo dsm
```

## Requirements
- Python 3.8 or higher
- Docker installed and running
- Required Python packages (installed automatically):
  - docker>=7.1.0
  - psutil>=7.0.0
  - tabulate>=0.9.0
  - matplotlib>=3.10.1
  - blessed>=1.20.0
  - py-cui>=0.1.6

## Interactive Menu Options

1. Service Management
   - Check service status
   - Start service
   - Stop service
   - Restart service
   - Enable service
   - Disable service

2. Socket Management
   - Check socket status
   - Manage Docker socket

3. Container Management
   - List containers
   - Remove containers
   - Prune stopped containers

4. Image Management
   - List images
   - Remove images
   - Prune dangling images

5. System Information
   - View Docker info
   - Check system status

6. Health Reports
   - Generate quick report
   - Generate full report

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Support
For issues and feature requests, please create an issue in the repository.
