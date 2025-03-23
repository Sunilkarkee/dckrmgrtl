#!/usr/bin/env python3
"""
Installation script for Docker Service Manager

This script automates the installation of Docker Service Manager
and its dependencies across all platforms (Windows, Linux, macOS).
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def is_windows():
    """Check if running on Windows."""
    return platform.system().lower() == 'windows'

def is_unix():
    """Check if running on Unix-like system."""
    return platform.system().lower() in ('linux', 'darwin')

def check_python_version():
    """Check if Python version meets requirements."""
    required_version = (3, 8)  # Updated to match setup.py
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current Python version is {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return False
    return True

def check_pip():
    """Check if pip is installed and up to date."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        return True
    except subprocess.CalledProcessError:
        print("Error: pip is not installed or not working correctly.")
        if is_windows():
            print("Please install pip from https://pip.pypa.io/en/stable/installation/")
        else:
            print("Please install pip using your package manager:")
            print("  - For Ubuntu/Debian: sudo apt install python3-pip")
            print("  - For Fedora: sudo dnf install python3-pip")
            print("  - For macOS: brew install python3")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    # Core dependencies
    dependencies = [
        "docker>=6.1.0",
        "psutil>=5.9.0",
        "tabulate>=0.9.0",
        "matplotlib>=3.7.0",
    ]
    
    # Optional dependencies
    optional_deps = [
        "blessed>=1.20.0",  # For TUI mode
    ]
    
    try:
        # Install core dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + dependencies)
        
        # Install optional dependencies if requested
        if args.with_tui:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + optional_deps)
        
        print("Dependencies installed successfully.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def install_package(editable=False):
    """Install the package."""
    print("Installing Docker Service Manager...")
    cmd = [sys.executable, "-m", "pip", "install"]
    
    if editable:
        cmd.append("-e")
    
    cmd.append(".")
    
    try:
        subprocess.check_call(cmd)
        print("Docker Service Manager installed successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e}")
        return False

def verify_installation():
    """Verify the installation by running a simple command."""
    try:
        print("Verifying installation...")
        # Import the module to verify it's installed correctly
        from importlib import import_module
        import_module("docker_manager")
        
        print("Docker Service Manager has been successfully installed!")
        print("\nTo use the tool, run one of the following commands:")
        print("  docker-service-manager --help")
        print("  python -m docker_manager.ui.cli --help")
        return True
    except ImportError as e:
        print(f"Error verifying installation: {e}")
        return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Install Docker Service Manager")
    parser.add_argument("--editable", "-e", action="store_true", 
                      help="Install in editable mode for development")
    parser.add_argument("--with-tui", action="store_true",
                      help="Install with TUI mode support")
    return parser.parse_args()

def main():
    """Main installation process."""
    global args
    args = parse_args()
    
    print("===============================================")
    print("Docker Service Manager - Installation")
    print("===============================================\n")
    
    print(f"Detected platform: {platform.system()} {platform.release()}")
    print(f"Python version: {sys.version.split()[0]}\n")
    
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    try:
        if not install_dependencies():
            sys.exit(1)
            
        if not install_package(args.editable):
            sys.exit(1)
            
        if not verify_installation():
            print("\nInstallation completed with warnings. Please check the output above.")
        else:
            print("\nInstallation completed successfully!")
            
    except Exception as e:
        print(f"\nError during installation: {e}")
        sys.exit(1)
    
    print("===============================================")
    
    if is_windows():
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()