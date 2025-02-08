import urllib.request
import json

API_KEY = "your_api_key_here"
search_field = "name"
search_value = "your_title_name_here"
# Fetch titles  info (title_id, year, etc) by name
url = f"https://api.watchmode.com/v1/search/?apiKey={API_KEY}&search_field={search_field}&search_value={search_value}"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    print(json.dumps(data, indent=4))


title_id = "your_title_id_here"
regions = "ES"  
# Fetch streaming sources available for the title_id
url = f"https://api.watchmode.com/v1/title/{title_id}/sources/?apiKey={API_KEY}&regions={regions}"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    print(json.dumps(data, indent=4))