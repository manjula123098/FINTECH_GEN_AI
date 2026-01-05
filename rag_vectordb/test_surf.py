import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_surf_api():
    api_key = os.getenv("SURF_API_KEY")
    
    if not api_key:
        print("❌ No SURF_API_KEY found in .env file")
        return False
    
    print(f"✅ SURF_API_KEY found: {api_key[:10]}...")
    
    # Test the API
    test_query = "latest developments in AI"
    url = "https://api.surfapi.com/search"
    
    headers = {
        'User-Agent': 'SchoolScienceRAG/1.0',
        'Accept': 'application/json'
    }
    
    params = {
        "q": test_query,
        "api_key": api_key,
        "num": 3,
        "format": "json"
    }
    
    try:
        print(f"🔍 Testing SURF API with query: '{test_query}'")
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📝 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ SUCCESS: Got {len(results)} results")
            
            for i, result in enumerate(results[:2], 1):
                print(f"   Result {i}: {result.get('title', 'No title')}")
                print(f"   Snippet: {result.get('snippet', result.get('description', 'No snippet'))[:100]}...")
                print()
            
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_surf_api()