"""
Command-line interface for Docker service manager.
"""
import argparse
import sys
import os
from typing import List, Dict, Optional, Any, Tuple

# Core imports
from ..core.service_manager import DockerServiceManager
from ..core.health_report import HealthReport
from ..core.container_logs import ContainerLogs
from ..core.container_manager import ContainerManager
from ..core.image_manager import ImageManager

# UI imports
from ..utils.display import show_banner, print_status

# Package imports
from .. import __version__

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

def setup_argparse() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Docker Service Manager - A cross-platform tool for managing Docker services"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode with simulated responses"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (default)"
    )
    return parser

def validate_input(args: argparse.Namespace) -> bool:
    """Validate command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        True if arguments are valid, False otherwise
    """
    return True

def process_args(args: argparse.Namespace) -> int:
    """Process command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        if args.interactive or not args.demo:
            return run_interactive_mode(args.demo)
        else:
            return run_demo_mode()
    except KeyboardInterrupt:
        print_status("Operation cancelled by user", "warning")
        return 1
    except Exception as e:
        print_status(f"Unexpected error: {str(e)}", "error")
        return 1

def run_interactive_mode(demo_mode: bool = False) -> int:
    """Run the application in interactive mode.
    
    Args:
        demo_mode: Whether to run in demo mode
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    show_banner()
    
    # Initialize managers
    service_manager = DockerServiceManager(demo_mode=demo_mode)
    container_manager = ContainerManager(demo_mode=demo_mode)
    image_manager = ImageManager(demo_mode=demo_mode)
    health_report = HealthReport(demo_mode=demo_mode)
    
    while True:
        print("\n=== Main Menu ===")
        print("-----------------")
        print("1. Service Management")
        print("2. Socket Management")
        print("3. Container Management")
        print("4. Image Management")
        print("5. System Information")
        print("6. Generate Health Report")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            return 0
        elif choice == '1':
            handle_service_management(service_manager)
        elif choice == '2':
            handle_socket_management(service_manager)
        elif choice == '3':
            handle_container_management(container_manager)
        elif choice == '4':
            handle_image_management(image_manager)
        elif choice == '5':
            handle_system_info(service_manager)
        elif choice == '6':
            handle_health_report(health_report)
        else:
            print_status("Invalid choice. Please try again.", "error")

def handle_container_management(container_manager: ContainerManager) -> None:
    """Handle container management menu.
    
    Args:
        container_manager: Container manager instance
    """
    while True:
        print("\n=== Container Management ===")
        print("---------------------------")
        print("1. List Running Containers")
        print("2. List All Containers")
        print("3. Remove Container")
        print("4. Remove All Stopped Containers")
        print("b. Back to Main Menu")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            sys.exit(0)
        elif choice == 'b':
            break
        elif choice == '1':
            containers = container_manager.list_containers(all_containers=False)
            if containers:
                print("\nRunning Containers:")
                print(tabulate(containers, headers="keys", tablefmt="grid"))
            else:
                print_status("No running containers found.", "info")
        elif choice == '2':
            containers = container_manager.list_containers(all_containers=True)
            if containers:
                print("\nAll Containers:")
                print(tabulate(containers, headers="keys", tablefmt="grid"))
            else:
                print_status("No containers found.", "info")
        elif choice == '3':
            container_id = input("Enter container ID or name to remove: ").strip()
            force = input("Force remove? (y/N): ").strip().lower() == 'y'
            if container_manager.remove_container(container_id, force):
                print_status("Container removed successfully.", "success")
            else:
                print_status("Failed to remove container.", "error")
        elif choice == '4':
            if input("Are you sure you want to remove all stopped containers? (y/N): ").strip().lower() == 'y':
                if container_manager.prune_containers():
                    print_status("All stopped containers removed successfully.", "success")
                else:
                    print_status("Failed to remove stopped containers.", "error")
        else:
            print_status("Invalid choice. Please try again.", "error")

def handle_image_management(image_manager: ImageManager) -> None:
    """Handle image management menu.
    
    Args:
        image_manager: Image manager instance
    """
    while True:
        print("\n=== Image Management ===")
        print("----------------------")
        print("1. List Images")
        print("2. Remove Image")
        print("3. Remove All Dangling Images")
        print("b. Back to Main Menu")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            sys.exit(0)
        elif choice == 'b':
            break
        elif choice == '1':
            images = image_manager.list_images()
            if images:
                print("\nDocker Images:")
                print(tabulate(images, headers="keys", tablefmt="grid"))
            else:
                print_status("No images found.", "info")
        elif choice == '2':
            image_id = input("Enter image ID or name:tag to remove: ").strip()
            force = input("Force remove? (y/N): ").strip().lower() == 'y'
            if image_manager.remove_image(image_id, force):
                print_status("Image removed successfully.", "success")
            else:
                print_status("Failed to remove image.", "error")
        elif choice == '3':
            if input("Are you sure you want to remove all dangling images? (y/N): ").strip().lower() == 'y':
                if image_manager.prune_images():
                    print_status("All dangling images removed successfully.", "success")
                else:
                    print_status("Failed to remove dangling images.", "error")
        else:
            print_status("Invalid choice. Please try again.", "error")

def handle_service_management(service_manager: DockerServiceManager) -> None:
    """Handle service management menu.
    
    Args:
        service_manager: Service manager instance
    """
    while True:
        print("\n=== Service Management ===")
        print("--------------------------")
        print("1. Check Service Status")
        print("2. Start Service")
        print("3. Stop Service")
        print("4. Restart Service")
        print("5. Enable Service")
        print("6. Disable Service")
        print("b. Back to Main Menu")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            sys.exit(0)
        elif choice == 'b':
            break
        elif choice == '1':
            success, error = service_manager.check_service_status()
            if not success:
                print_status(f"Error checking service status: {error}", "error")
        elif choice == '2':
            if service_manager.start_service():
                print_status("Service started successfully.", "success")
            else:
                print_status("Failed to start service.", "error")
        elif choice == '3':
            if service_manager.stop_service():
                print_status("Service stopped successfully.", "success")
            else:
                print_status("Failed to stop service.", "error")
        elif choice == '4':
            if service_manager.restart_service():
                print_status("Service restarted successfully.", "success")
            else:
                print_status("Failed to restart service.", "error")
        elif choice == '5':
            if service_manager.enable_service():
                print_status("Service enabled successfully.", "success")
            else:
                print_status("Failed to enable service.", "error")
        elif choice == '6':
            if service_manager.disable_service():
                print_status("Service disabled successfully.", "success")
            else:
                print_status("Failed to disable service.", "error")
        else:
            print_status("Invalid choice. Please try again.", "error")

def handle_socket_management(service_manager: DockerServiceManager) -> None:
    """Handle socket management menu.
    
    Args:
        service_manager: Service manager instance
    """
    while True:
        print("\n=== Socket Management ===")
        print("-------------------------")
        print("1. Check Socket Status")
        print("2. Start Socket")
        print("3. Stop Socket")
        print("4. Restart Socket")
        print("b. Back to Main Menu")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            sys.exit(0)
        elif choice == 'b':
            break
        elif choice == '1':
            success, error = service_manager.check_socket_status()
            if not success:
                print_status(f"Error checking socket status: {error}", "error")
        elif choice == '2':
            if service_manager.start_socket():
                print_status("Socket started successfully.", "success")
            else:
                print_status("Failed to start socket.", "error")
        elif choice == '3':
            if service_manager.stop_socket():
                print_status("Socket stopped successfully.", "success")
            else:
                print_status("Failed to stop socket.", "error")
        elif choice == '4':
            if service_manager.restart_socket():
                print_status("Socket restarted successfully.", "success")
            else:
                print_status("Failed to restart socket.", "error")
        else:
            print_status("Invalid choice. Please try again.", "error")

def handle_system_info(service_manager: DockerServiceManager) -> None:
    """Handle system information menu.
    
    Args:
        service_manager: Service manager instance
    """
    while True:
        print("\n=== System Information ===")
        print("-------------------------")
        print("1. Show Docker Info")
        print("2. Show System Resources")
        print("b. Back to Main Menu")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            sys.exit(0)
        elif choice == 'b':
            break
        elif choice == '1':
            success, error = service_manager.show_docker_info()
            if not success:
                print_status(f"Error showing Docker info: {error}", "error")
        elif choice == '2':
            success, error = service_manager.show_system_resources()
            if not success:
                print_status(f"Error showing system resources: {error}", "error")
        else:
            print_status("Invalid choice. Please try again.", "error")

def handle_health_report(health_report: HealthReport) -> None:
    """Handle health report menu.
    
    Args:
        health_report: Health report instance
    """
    while True:
        print("\n=== Health Report ===")
        print("-------------------")
        print("1. Generate Full Report")
        print("2. Generate Quick Report")
        print("b. Back to Main Menu")
        print("q. Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print_status("Goodbye!", "info")
            sys.exit(0)
        elif choice == 'b':
            break
        elif choice == '1':
            success, error = health_report.generate_full_report()
            if not success:
                print_status(f"Error generating full report: {error}", "error")
        elif choice == '2':
            success, error = health_report.generate_quick_report()
            if not success:
                print_status(f"Error generating quick report: {error}", "error")
        else:
            print_status("Invalid choice. Please try again.", "error")

def run_demo_mode() -> int:
    """Run the application in demo mode.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    print("\033[93mDEMO MODE\033[0m: Running with simulated responses")
    return run_interactive_mode(demo_mode=True)

def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Set up argument parser
        parser = setup_argparse()
        
        # Parse arguments
        args = parser.parse_args()
        
        # Validate arguments
        if not validate_input(args):
            return 1
            
        # Process arguments
        return process_args(args)
        
    except KeyboardInterrupt:
        print_status("Operation cancelled by user", "warning")
        return 1
    except Exception as e:
        print_status(f"Unexpected error: {str(e)}", "error")
        return 1

if __name__ == '__main__':
    sys.exit(main())
