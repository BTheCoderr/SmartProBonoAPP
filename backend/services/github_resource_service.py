"""
GitHub Resource Service for managing templates stored in GitHub Releases.
"""
import os
import requests
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class GitHubResourceService:
    """Service for interacting with GitHub Releases to manage templates."""
    
    def __init__(self, repo=None, token=None):
        """
        Initialize the GitHub resource service.
        
        Args:
            repo: GitHub repository in format "owner/repo" (default: from env var)
            token: GitHub API token for private repos (default: from env var)
        """
        self.repo = repo or os.environ.get("GITHUB_REPO", "SmartProBonoProject/SmartProBono")
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_base_url = f"https://api.github.com/repos/{self.repo}"
        self.download_base_url = f"https://github.com/{self.repo}/releases/download"
        
        # Create cache directory in user's home directory
        self.cache_dir = Path(os.path.expanduser("~/.smartprobono/cache"))
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Configure request headers
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def get_releases(self):
        """
        Get all available releases.
        
        Returns:
            List of release dictionaries from GitHub API
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/releases",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching releases: {e}")
            return []
    
    def get_latest_release(self):
        """
        Get the latest release.
        
        Returns:
            Dictionary of release details or None if not found
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/releases/latest",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching latest release: {e}")
            return None
    
    def get_release_by_tag(self, tag):
        """
        Get a specific release by tag name.
        
        Args:
            tag: The release tag (e.g., 'v1.0.0')
            
        Returns:
            Dictionary of release details or None if not found
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/releases/tags/{tag}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching release {tag}: {e}")
            return None
    
    def get_template(self, template_name, version="latest"):
        """
        Download a template file from GitHub releases.
        
        Args:
            template_name: Name of the template file
            version: Release tag (e.g., 'v1.0.0') or 'latest'
            
        Returns:
            Path to the downloaded file or None if failed
        """
        # Check cache first
        cache_key = f"{version}_{template_name}".replace("/", "_")
        cache_path = self.cache_dir / cache_key
        
        if cache_path.exists():
            logger.info(f"Using cached template: {cache_path}")
            return str(cache_path)
        
        # Get the release info to find the asset
        if version == "latest":
            release = self.get_latest_release()
            if not release:
                logger.error("Latest release not found")
                return None
            version = release["tag_name"]
        else:
            release = self.get_release_by_tag(version)
            if not release:
                logger.error(f"Release {version} not found")
                return None
        
        # Download the asset if it exists
        download_url = f"{self.download_base_url}/{version}/{template_name}"
        try:
            logger.info(f"Downloading template: {download_url}")
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Template downloaded to: {cache_path}")
            return str(cache_path)
        
        except requests.RequestException as e:
            logger.error(f"Error downloading template {template_name}: {e}")
            return None
    
    def list_templates(self, version="latest", category=None):
        """
        List all templates in a release.
        
        Args:
            version: Release tag or 'latest'
            category: Optional category filter (e.g., 'legal', 'housing')
            
        Returns:
            List of template dictionaries with metadata
        """
        # Get the release
        if version == "latest":
            release = self.get_latest_release()
        else:
            release = self.get_release_by_tag(version)
            
        if not release:
            logger.error(f"Release {version} not found")
            return []
        
        # Get assets from the release
        assets = release.get("assets", [])
        
        # Process and filter assets
        templates = []
        for asset in assets:
            name = asset["name"]
            
            # Skip non-template files if needed
            if not (name.endswith('.txt') or name.endswith('.md') or 
                    name.endswith('.pdf') or name.endswith('.docx')):
                continue
                
            # Apply category filter if specified
            if category and not name.startswith(f"{category}/"):
                continue
                
            templates.append({
                "name": name,
                "size": asset["size"],
                "download_url": asset["browser_download_url"],
                "created_at": asset["created_at"],
                "updated_at": asset.get("updated_at", asset["created_at"]),
                "download_count": asset["download_count"]
            })
        
        return templates
    
    def search_templates(self, query, version="latest"):
        """
        Search templates by name.
        
        Args:
            query: Search term
            version: Release tag or 'latest'
            
        Returns:
            List of matching templates
        """
        templates = self.list_templates(version=version)
        
        if not query:
            return templates
            
        query = query.lower()
        return [
            template for template in templates
            if query in template["name"].lower()
        ]
    
    def clear_cache(self, template_name=None, version=None):
        """
        Clear the template cache.
        
        Args:
            template_name: Specific template to clear (or all if None)
            version: Specific version to clear (or all if None)
            
        Returns:
            Number of files cleared
        """
        count = 0
        
        if template_name and version:
            # Clear specific template version
            cache_key = f"{version}_{template_name}".replace("/", "_")
            cache_path = self.cache_dir / cache_key
            if cache_path.exists():
                cache_path.unlink()
                count = 1
        elif template_name:
            # Clear all versions of a template
            for path in self.cache_dir.glob(f"*_{template_name.replace('/', '_')}"):
                path.unlink()
                count += 1
        elif version:
            # Clear all templates from a version
            for path in self.cache_dir.glob(f"{version}_*"):
                path.unlink()
                count += 1
        else:
            # Clear all cached templates
            for path in self.cache_dir.glob("*"):
                if path.is_file():
                    path.unlink()
                    count += 1
        
        return count 