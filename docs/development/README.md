# Docker Service Manager Development Guide

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Docker installed and running
- Git
- Virtual environment (recommended)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/docker-service-manager.git
cd docker-service-manager
```

2. Create and activate virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Linux/macOS
# or
myenv\Scripts\activate  # On Windows
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Install package in development mode:
```bash
pip install -e .
```

## Project Structure

```
docker_manager/
├── core/           # Core functionality
├── ui/             # User interface
├── utils/          # Utilities
└── __init__.py     # Package initialization

tests/              # Test files
docs/               # Documentation
    ├── api/        # API documentation
    ├── guides/     # User guides
    └── development/# Development guides
```

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Use pytest for testing
- Mock external dependencies

### Documentation
- Update documentation for new features
- Keep API documentation current
- Add examples for new functionality
- Update changelog

## Adding New Features

1. Create feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Implement feature:
   - Add new module if needed
   - Update existing modules
   - Add tests
   - Update documentation

3. Run tests:
```bash
pytest
```

4. Check code style:
```bash
flake8
mypy .
```

5. Commit changes:
```bash
git add .
git commit -m "Add: your feature description"
```

6. Push changes:
```bash
git push origin feature/your-feature-name
```

7. Create pull request

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_service_manager.py

# Run with coverage
pytest --cov=docker_manager

# Run with verbose output
pytest -v
```

### Writing Tests
```python
def test_feature():
    # Arrange
    manager = DockerServiceManager()
    
    # Act
    result = manager.some_method()
    
    # Assert
    assert result == expected_value
```

## Building and Distribution

### Building Package
```bash
# Build package
python setup.py build

# Create distribution
python setup.py sdist bdist_wheel
```

### Publishing to PyPI
```bash
# Upload to PyPI
twine upload dist/*
```

## Contributing

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Update documentation
6. Submit pull request

### Code Review Guidelines
- Check code style
- Verify tests pass
- Ensure documentation is updated
- Review for security issues
- Check performance impact

## Release Process

1. Update version in:
   - `setup.py`
   - `docker_manager/__init__.py`
   - `CHANGELOG.md`

2. Create release branch:
```bash
git checkout -b release/v1.x.x
```

3. Update documentation

4. Create release on GitHub

5. Build and publish to PyPI

## Support

### Getting Help
- Check documentation
- Review existing issues
- Create new issue if needed
- Join discussions

### Reporting Issues
1. Check if issue exists
2. Provide detailed description
3. Include steps to reproduce
4. Add system information
5. Attach logs if relevant

## License

MIT License - See LICENSE file for details 