"""
Container management functionality for Docker service manager.
"""
import sys
from typing import List, Dict, Optional, Any, Tuple

try:
    import docker
    from docker.errors import DockerException
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


class ContainerManager:
    """Container management functionality for Docker."""
    
    def __init__(self, demo_mode: bool = False):
        """Initialize container manager.
        
        Args:
            demo_mode: Whether to use demo mode with simulated responses
        """
        self.demo_mode = demo_mode
        self.client = None if demo_mode else docker.from_env()
        
    def list_containers(self, all_containers: bool = False) -> List[Dict[str, Any]]:
        """List all containers.
        
        Args:
            all_containers: Whether to show all containers (including stopped ones)
            
        Returns:
            List of container dictionaries
        """
        if self.demo_mode:
            print("\033[93mDEMO MODE\033[0m: Simulating container list")
            return [
                {
                    "ID": "abc123",
                    "Name": "web-server",
                    "Status": "running",
                    "Image": "nginx:latest",
                    "Created": "2 hours ago"
                },
                {
                    "ID": "def456",
                    "Name": "db-server",
                    "Status": "stopped",
                    "Image": "postgres:13",
                    "Created": "1 day ago"
                }
            ]
            
        try:
            containers = self.client.containers.list(all=all_containers)
            return [
                {
                    "ID": c.id[:12],
                    "Name": c.name,
                    "Status": c.status,
                    "Image": c.image.tags[0] if c.image.tags else c.image.id[:12],
                    "Created": c.attrs['Created']
                }
                for c in containers
            ]
        except DockerException as e:
            print(f"Error listing containers: {str(e)}")
            return []
            
    def remove_container(self, container_id: str, force: bool = False) -> bool:
        """Remove a container.
        
        Args:
            container_id: Container ID or name
            force: Whether to force remove (kill if running)
            
        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            print(f"\033[93mDEMO MODE\033[0m: Simulating container removal '{container_id}'")
            return True
            
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            return True
        except DockerException as e:
            print(f"Error removing container: {str(e)}")
            return False
            
    def prune_containers(self) -> bool:
        """Remove all stopped containers.
        
        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            print("\033[93mDEMO MODE\033[0m: Simulating container pruning")
            return True
            
        try:
            self.client.containers.prune()
            return True
        except DockerException as e:
            print(f"Error pruning containers: {str(e)}")
            return False 