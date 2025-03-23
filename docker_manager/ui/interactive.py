"""
Interactive console UI for Docker service manager.
"""
import os
import sys
import time
from typing import List, Dict, Callable, Any, Optional

from ..core.service_manager import DockerServiceManager
from ..core.health_report import HealthReport
from ..core.container_visualization import ContainerVisualizer
from ..utils.display import COLORS, get_terminal_size, show_banner, print_status, print_section
from .onboarding import OnboardingManager

class InteractiveConsole:
    """Interactive console interface for Docker service management."""
    
    def __init__(self, demo_mode: bool = False):
        """Initialize interactive console.
        
        Args:
            demo_mode: Whether to use demo mode for Docker operations
        """
        self.manager = DockerServiceManager(demo_mode=demo_mode)
        self.onboarding = OnboardingManager(demo_mode=demo_mode)
        self.demo_mode = demo_mode
        self.running = True
        self.current_menu = "main"
        self.menus = self._create_menus()

    def _create_menus(self) -> Dict[str, Dict[str, Any]]:
        """Create menu structure with options and actions.
        
        Returns:
            Dictionary of menus with their options and associated actions
        """
        return {
            "main": {
                "title": "Main Menu",
                "options": [
                    {"key": "1", "desc": "Service Management", "action": lambda: self._change_menu("service")},
                    {"key": "2", "desc": "Socket Management", "action": lambda: self._change_menu("socket")},
                    {"key": "3", "desc": "Container Management", "action": lambda: self._change_menu("container")},
                    {"key": "4", "desc": "System Information", "action": lambda: self._change_menu("info")},
                    {"key": "5", "desc": "Generate Health Report", "action": self._generate_health_report},
                    {"key": "q", "desc": "Quit", "action": self._quit},
                ],
            },
            "service": {
                "title": "Service Management",
                "options": [
                    {"key": "1", "desc": "Check Service Status", "action": self._check_service_status},
                    {"key": "2", "desc": "Start Service", "action": self._start_service},
                    {"key": "3", "desc": "Stop Service", "action": self._stop_service},
                    {"key": "4", "desc": "Restart Service", "action": self._restart_service},
                    {"key": "5", "desc": "Enable Service", "action": self._enable_service},
                    {"key": "6", "desc": "Disable Service", "action": self._disable_service},
                    {"key": "b", "desc": "Back to Main Menu", "action": lambda: self._change_menu("main")},
                    {"key": "q", "desc": "Quit", "action": self._quit},
                ],
            },
            "socket": {
                "title": "Socket Management",
                "options": [
                    {"key": "1", "desc": "Check Socket Status", "action": self._check_socket_status},
                    {"key": "2", "desc": "Start Socket", "action": self._start_socket},
                    {"key": "3", "desc": "Stop Socket", "action": self._stop_socket},
                    {"key": "4", "desc": "Enable Socket", "action": self._enable_socket},
                    {"key": "5", "desc": "Disable Socket", "action": self._disable_socket},
                    {"key": "b", "desc": "Back to Main Menu", "action": lambda: self._change_menu("main")},
                    {"key": "q", "desc": "Quit", "action": self._quit},
                ],
            },
            "container": {
                "title": "Container Management",
                "options": [
                    {"key": "1", "desc": "List Containers", "action": self._list_containers},
                    {"key": "2", "desc": "View Container Logs", "action": self._view_container_logs},
                    {"key": "3", "desc": "Visualize Containers", "action": self._visualize_containers},
                    {"key": "b", "desc": "Back to Main Menu", "action": lambda: self._change_menu("main")},
                    {"key": "q", "desc": "Quit", "action": self._quit},
                ],
            },
            "info": {
                "title": "System Information",
                "options": [
                    {"key": "1", "desc": "Show Docker Info", "action": self._show_docker_info},
                    {"key": "2", "desc": "Check Privileges", "action": self._check_privileges},
                    {"key": "b", "desc": "Back to Main Menu", "action": lambda: self._change_menu("main")},
                    {"key": "q", "desc": "Quit", "action": self._quit},
                ],
            },
        }

    def _clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _change_menu(self, menu_name: str) -> None:
        """Change the current menu.
        
        Args:
            menu_name: Name of the menu to switch to
        """
        if menu_name in self.menus:
            self.current_menu = menu_name
            self._clear_screen()
        else:
            print_status(f"Invalid menu: {menu_name}", "error")

    def _display_menu(self) -> None:
        """Display the current menu."""
        show_banner()
        
        menu = self.menus[self.current_menu]
        print_section(menu["title"])
        
        for option in menu["options"]:
            print(f"{COLORS['CYAN']}{option['key']}{COLORS['RESET']}. {option['desc']}")
        
        print("\nEnter your choice: ", end="", flush=True)

    def _get_input(self) -> str:
        """Get user input.
        
        Returns:
            User's input choice
        """
        try:
            return input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "q"

    def _process_action(self, choice: str) -> None:
        """Process the user's menu choice.
        
        Args:
            choice: User's input choice
        """
        menu = self.menus[self.current_menu]
        
        for option in menu["options"]:
            if option["key"] == choice:
                try:
                    option["action"]()
                except Exception as e:
                    print_status(f"Error executing action: {str(e)}", "error")
                    if self.demo_mode:
                        print("Try running without --demo flag")
                return
        
        print_status("Invalid choice", "error")

    def _quit(self) -> None:
        """Quit the application."""
        self.running = False
        print_status("Goodbye!", "info")

    def _handle_action_result(self, success: bool, action_name: str, error_code: Optional[str] = None) -> None:
        """Handle the result of an action.
        
        Args:
            success: Whether the action was successful
            action_name: Name of the action
            error_code: Optional error code for failed actions
        """
        if success:
            print_status(f"{action_name} completed successfully", "success")
        else:
            error_msg = f"{action_name} failed"
            if error_code:
                error_msg += f" (Error: {error_code})"
            print_status(error_msg, "error")
            
            if self.demo_mode:
                print("Try running without --demo flag")

    def _check_service_status(self) -> None:
        """Check Docker service status."""
        success = self.manager.get_status()
        self._handle_action_result(success, "Service status check")
        
        if success:
            input("\nPress Enter to continue...")

    def _start_service(self) -> None:
        """Start Docker service."""
        success = self.manager.start_service()
        self._handle_action_result(success, "Service start")

    def _stop_service(self) -> None:
        """Stop Docker service."""
        success = self.manager.stop_service()
        self._handle_action_result(success, "Service stop")

    def _restart_service(self) -> None:
        """Restart Docker service."""
        success = self.manager.restart_service()
        self._handle_action_result(success, "Service restart")

    def _enable_service(self) -> None:
        """Enable Docker service."""
        success = self.manager.enable_service()
        self._handle_action_result(success, "Service enable")

    def _disable_service(self) -> None:
        """Disable Docker service."""
        success = self.manager.disable_service()
        self._handle_action_result(success, "Service disable")

    def _check_socket_status(self) -> None:
        """Check Docker socket status."""
        success = self.manager.get_socket_status()
        self._handle_action_result(success, "Socket status check")
        
        if success:
            input("\nPress Enter to continue...")

    def _start_socket(self) -> None:
        """Start Docker socket."""
        success = self.manager.start_socket()
        self._handle_action_result(success, "Socket start")

    def _stop_socket(self) -> None:
        """Stop Docker socket."""
        success = self.manager.stop_socket()
        self._handle_action_result(success, "Socket stop")

    def _enable_socket(self) -> None:
        """Enable Docker socket."""
        success = self.manager.enable_socket()
        self._handle_action_result(success, "Socket enable")

    def _disable_socket(self) -> None:
        """Disable Docker socket."""
        success = self.manager.disable_socket()
        self._handle_action_result(success, "Socket disable")

    def _list_containers(self) -> None:
        """List Docker containers."""
        success = self.manager.list_containers()
        self._handle_action_result(success, "Container listing")
        
        if success:
            input("\nPress Enter to continue...")

    def _view_container_logs(self) -> None:
        """View container logs."""
        # Get list of containers
        containers = self.manager.get_containers()
        if not containers:
            print_status("No containers found", "warning")
            return
            
        # Display container list
        print_section("Available Containers")
        for i, container in enumerate(containers, 1):
            name = container.get("name", container.get("id", "Unknown"))
            status = container.get("status", "Unknown")
            print(f"{i}. {name} ({status})")
            
        # Get container selection
        try:
            choice = input("\nEnter container number (or 'b' to go back): ").strip()
            if choice.lower() == 'b':
                return
                
            index = int(choice) - 1
            if 0 <= index < len(containers):
                container = containers[index]
                container_id = container.get("id")
                
                # Get number of lines
                lines = input("Enter number of lines to show (default: 100): ").strip()
                lines = int(lines) if lines.isdigit() else 100
                
                # View logs
                success = self.manager.get_container_logs(container_id, tail=lines)
                self._handle_action_result(success, "Log viewing")
                
                if success:
                    input("\nPress Enter to continue...")
            else:
                print_status("Invalid container number", "error")
        except ValueError:
            print_status("Invalid input", "error")
        except Exception as e:
            print_status(f"Error viewing logs: {str(e)}", "error")

    def _visualize_containers(self) -> None:
        """Visualize container metrics."""
        try:
            visualizer = ContainerVisualizer(demo_mode=self.demo_mode)
            success = visualizer.generate_visualizations()
            self._handle_action_result(success, "Container visualization")
            
            if success:
                input("\nPress Enter to continue...")
        except Exception as e:
            print_status(f"Error generating visualizations: {str(e)}", "error")

    def _show_docker_info(self) -> None:
        """Show Docker system information."""
        success = self.manager.check_docker_info()
        self._handle_action_result(success, "Docker info")
        
        if success:
            input("\nPress Enter to continue...")

    def _check_privileges(self) -> None:
        """Check if user has necessary privileges."""
        success = self.manager.check_privileges()
        self._handle_action_result(success, "Privilege check")

    def _generate_health_report(self) -> None:
        """Generate system health report."""
        try:
            health_reporter = HealthReport(demo_mode=self.demo_mode)
            success = health_reporter.generate_report()
            self._handle_action_result(success, "Health report generation")
            
            if success:
                input("\nPress Enter to continue...")
        except Exception as e:
            print_status(f"Error generating health report: {str(e)}", "error")

    def run(self) -> None:
        """Run the interactive console."""
        try:
            while self.running:
                self._display_menu()
                choice = self._get_input()
                self._process_action(choice)
                
        except Exception as e:
            print_status(f"Unexpected error: {str(e)}", "error")
            if self.demo_mode:
                print("Try running without --demo flag")
            sys.exit(1)