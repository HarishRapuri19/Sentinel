# src/databricks_client.py
import requests
from src.config import CONFIG

class DatabricksClient:
    def __init__(self):
        print("[System] Initializing Databricks REST Client...")
        
        raw_host = CONFIG.get("DATABRICKS_HOST", "")
        raw_token = CONFIG.get("DATABRICKS_TOKEN", "")
        
        # ARCHITECT FIX: Automatically sanitize inputs
        # 1. Strip trailing slashes and whitespace from host
        self.host = raw_host.rstrip('/').strip()
        
        # 2. Strip accidental quotes or spaces from the token
        self.token = raw_token.replace('"', '').replace("'", "").strip()
        
        if not self.host or not self.token:
            raise ValueError("[ERROR] Databricks Host or Token is missing in .env")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def test_connection(self):
        """Pings the Databricks 'Clusters' API to validate the token."""
        print(f"[System] Pinging Databricks Workspace at: {self.host}")
        
        # Changed from the SCIM (User) API to the Clusters API
        endpoint = f"{self.host}/api/2.0/clusters/list"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10, allow_redirects=False)
            
            if response.status_code == 200:
                clusters = response.json().get("clusters", [])
                print(f"[Success] API Handshake Complete! Found {len(clusters)} cluster(s).")
                return True
            else:
                print(f"[FAILED] Databricks rejected the token. HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"[CRITICAL] Network error while reaching Databricks: {e}")
            return False

if __name__ == "__main__":
    client = DatabricksClient()
    client.test_connection()