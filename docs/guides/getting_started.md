# Getting Started with Docker Service Manager

## Installation

### Prerequisites
- Python 3.8 or higher
- Docker installed and running
- Git (for cloning the repository)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/docker-service-manager.git
cd docker-service-manager
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv myenv
source myenv/bin/activate  # On Linux/macOS
# or
myenv\Scripts\activate  # On Windows
```

3. Install the package:
```bash
pip install -e .
```

## Quick Start

### Basic Usage
```bash
dsm
```

### Running with Administrative Privileges
For full functionality:
```bash
sudo dsm  # On Linux/macOS
```

### Command Line Options
```bash
dsm --help        # Show help message
dsm --version     # Show version information
dsm --interactive # Run in interactive mode (default)
dsm --demo       # Run in demo mode
```

## Basic Operations

### 1. Service Management
```bash
# Check service status
dsm --interactive
# Select option 1: Service Management
# Select option 1: Check Service Status
```

### 2. Container Management
```bash
# List running containers
dsm --interactive
# Select option 3: Container Management
# Select option 1: List Running Containers
```

### 3. Image Management
```bash
# List Docker images
dsm --interactive
# Select option 4: Image Management
# Select option 1: List Images
```

## Next Steps

1. Read the [User Guide](user_guide.md) for detailed information about all features
2. Check the [API Reference](../api/README.md) for developer documentation
3. Visit the [Development Guide](../development/README.md) if you want to contribute

## Troubleshooting

### Common Issues

1. Permission Denied
   - Solution: Run with sudo or add your user to the docker group
   ```bash
   sudo usermod -aG docker $USER
   ```

2. Docker Not Running
   - Solution: Start the Docker service
   ```bash
   sudo systemctl start docker
   ```

3. Module Not Found
   - Solution: Ensure you're in the virtual environment and the package is installed
   ```bash
   source myenv/bin/activate
   pip install -e .
   ``` 