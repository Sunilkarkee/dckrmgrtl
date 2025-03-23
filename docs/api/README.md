# Docker Service Manager API Reference

## Core Modules

### Service Manager
```python
from docker_manager.core.service_manager import DockerServiceManager

# Initialize service manager
manager = DockerServiceManager(demo_mode=False)

# Service operations
manager.check_service_status()
manager.start_service()
manager.stop_service()
manager.restart_service()
manager.enable_service()
manager.disable_service()
```

### Container Manager
```python
from docker_manager.core.container_manager import ContainerManager

# Initialize container manager
manager = ContainerManager(demo_mode=False)

# Container operations
manager.list_containers(all_containers=False)
manager.remove_container(container_id, force=False)
manager.prune_containers()
```

### Image Manager
```python
from docker_manager.core.image_manager import ImageManager

# Initialize image manager
manager = ImageManager(demo_mode=False)

# Image operations
manager.list_images()
manager.remove_image(image_id, force=False)
manager.prune_images()
```

### Health Report
```python
from docker_manager.core.health_report import HealthReport

# Initialize health report
report = HealthReport(demo_mode=False)

# Generate reports
report.generate_quick_report()
report.generate_full_report()
```

## UI Components

### CLI Interface
```python
from docker_manager.ui.cli import main

# Run CLI
main()
```

### Interactive Mode
```python
from docker_manager.ui.interactive import run_interactive_mode

# Run interactive mode
run_interactive_mode(demo_mode=False)
```

## Utility Functions

### Display Utilities
```python
from docker_manager.utils.display import show_banner, print_status

# Display functions
show_banner()
print_status("Message", "info|success|warning|error")
```

### System Utilities
```python
from docker_manager.utils.system import get_system_info

# System information
info = get_system_info()
```

## Project Structure

```
docker_manager/
├── __init__.py             # Package initialization
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── service_manager.py  # Service management
│   ├── container_manager.py # Container management
│   ├── image_manager.py    # Image management
│   └── health_report.py    # Health reporting
├── ui/                     # User interface
│   ├── __init__.py
│   ├── cli.py             # CLI implementation
│   └── interactive.py     # Interactive mode
└── utils/                 # Utilities
    ├── __init__.py
    ├── display.py        # Display utilities
    └── system.py         # System utilities
```

## Development

### Adding New Features

1. Create new module in appropriate directory
2. Implement required functionality
3. Add tests in `tests/` directory
4. Update documentation
5. Add entry points in `setup.py`

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=docker_manager
```

### Building

```bash
# Build package
python setup.py build

# Create distribution
python setup.py sdist bdist_wheel
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Update documentation
6. Submit pull request

## License

MIT License - See LICENSE file for details 