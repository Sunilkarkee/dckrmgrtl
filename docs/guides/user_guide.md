# Docker Service Manager User Guide

## Overview

Docker Service Manager (DSM) is a powerful tool for managing Docker services, containers, and images. This guide provides detailed information about all features and how to use them effectively.

## Main Features

### 1. Service Management

#### Service Status
- Check current status of Docker service
- View detailed service information
- Monitor service health

#### Service Control
- Start Docker service
- Stop Docker service
- Restart Docker service
- Enable service at boot
- Disable service at boot

### 2. Container Management

#### Container Listing
- List running containers
- List all containers (including stopped)
- View container details:
  - Container ID
  - Name
  - Status
  - Image
  - Ports
  - Created time

#### Container Operations
- Remove specific containers
- Force remove containers
- Prune stopped containers
- View container logs

### 3. Image Management

#### Image Operations
- List all Docker images
- Remove specific images
- Force remove images
- Prune dangling images
- View image details:
  - Image ID
  - Repository
  - Tag
  - Size
  - Created time

### 4. System Information

#### Docker System Info
- Docker version
- API version
- OS information
- Architecture
- CPU/GPU information
- Memory usage
- Storage information

#### Resource Monitoring
- CPU usage
- Memory usage
- Disk usage
- Network statistics

### 5. Health Reports

#### Report Types
- Quick Report
  - Basic system status
  - Service status
  - Container count
  - Image count

- Full Report
  - Detailed system metrics
  - Resource usage graphs
  - Performance statistics
  - Health recommendations

## Interactive Mode

### Navigation
- Use number keys to select options
- Press 'q' to quit
- Press 'b' to go back
- Press 'h' for help

### Menu Structure
1. Service Management
2. Socket Management
3. Container Management
4. Image Management
5. System Information
6. Health Reports

## Command Line Options

```bash
dsm [options]

Options:
  --help        Show help message
  --version     Show version information
  --interactive Run in interactive mode (default)
  --demo        Run in demo mode
```

## Best Practices

1. Service Management
   - Always check service status before operations
   - Use sudo for service control operations
   - Enable service at boot for production systems

2. Container Management
   - Regularly prune stopped containers
   - Use force remove with caution
   - Monitor container logs for issues

3. Image Management
   - Keep images updated
   - Remove unused images
   - Use specific tags for images

4. System Monitoring
   - Generate health reports regularly
   - Monitor resource usage
   - Check system logs for issues

## Troubleshooting

### Common Issues

1. Permission Issues
   ```bash
   sudo usermod -aG docker $USER
   ```

2. Service Not Starting
   ```bash
   sudo systemctl status docker
   sudo systemctl start docker
   ```

3. Resource Issues
   - Check system resources
   - Prune unused containers/images
   - Monitor resource usage

## Support

For additional help:
- Check the [API Reference](../api/README.md)
- Visit the [Development Guide](../development/README.md)
- Create an issue in the repository 