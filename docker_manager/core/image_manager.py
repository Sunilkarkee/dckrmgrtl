"""
Image management functionality for Docker service manager.
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


class ImageManager:
    """Image management functionality for Docker."""
    
    def __init__(self, demo_mode: bool = False):
        """Initialize image manager.
        
        Args:
            demo_mode: Whether to use demo mode with simulated responses
        """
        self.demo_mode = demo_mode
        self.client = None if demo_mode else docker.from_env()
            
    def list_images(self) -> List[Dict[str, Any]]:
        """List all Docker images.
        
        Returns:
            List of image dictionaries
        """
        if self.demo_mode:
            print("\033[93mDEMO MODE\033[0m: Simulating image list")
            return [
                {
                    "ID": "abc123",
                    "Repository": "nginx",
                    "Tag": "latest",
                    "Size": "133MB",
                    "Created": "2 days ago"
                },
                {
                    "ID": "def456",
                    "Repository": "postgres",
                    "Tag": "13",
                    "Size": "376MB",
                    "Created": "1 week ago"
                }
            ]
            
        try:
            images = self.client.images.list()
            return [
                {
                    "ID": img.id[7:19],
                    "Repository": img.tags[0].split(':')[0] if img.tags else "<none>",
                    "Tag": img.tags[0].split(':')[1] if img.tags else "<none>",
                    "Size": f"{img.attrs['Size'] / 1024 / 1024:.1f}MB",
                    "Created": img.attrs['Created']
                }
                for img in images
            ]
        except DockerException as e:
            print(f"Error listing images: {str(e)}")
            return []
            
    def remove_image(self, image_id: str, force: bool = False) -> bool:
        """Remove a Docker image.
        
        Args:
            image_id: Image ID or name:tag
            force: Whether to force remove
            
        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            print(f"\033[93mDEMO MODE\033[0m: Simulating image removal '{image_id}'")
            return True
            
        try:
            self.client.images.remove(image_id, force=force)
            return True
        except DockerException as e:
            print(f"Error removing image: {str(e)}")
            return False
            
    def prune_images(self) -> bool:
        """Remove all dangling images.
        
        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            print("\033[93mDEMO MODE\033[0m: Simulating image pruning")
            return True
            
        try:
            self.client.images.prune()
            return True
        except DockerException as e:
            print(f"Error pruning images: {str(e)}")
            return False 