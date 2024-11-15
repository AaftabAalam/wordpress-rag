import requests
from typing import List, Dict

class WordPressIntegration:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_posts(self) -> List[Dict]:
        """Fetch all posts from the WordPress site."""
        try:
            response = requests.get(f"{self.base_url}/wp-json/wp/v2/posts")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching posts: {e}")
            return []

    def fetch_post_by_id(self, post_id: int) -> Dict:
        """Fetch a single post by its ID."""
        try:
            response = requests.get(f"{self.base_url}/wp-json/wp/v2/posts/{post_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching post with ID {post_id}: {e}")
            return {}