import logging
import asyncio

BASE_URL = "https://2025electionresults.comelec.gov.ph/data"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def fetch_json(client, url):
    try:
        # Add a small delay to avoid triggering anti-bot measures
        await asyncio.sleep(0.5)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://2025electionresults.comelec.gov.ph/',
            'Origin': 'https://2025electionresults.comelec.gov.ph'
        }
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return None

async def fetch_regions(client):
    # First visit the main site to establish a session
    try:
        await client.get("https://2025electionresults.comelec.gov.ph/")
        await asyncio.sleep(2)  # Wait a bit for any initial setup
    except:
        pass  # Ignore errors from the main page
    
    return await fetch_json(client, f"{BASE_URL}/regions/local/0.json")

async def fetch_provinces(client, region_code):
    return await fetch_json(client, f"{BASE_URL}/regions/local/{region_code}.json")

async def fetch_cities(client, province_code):
    return await fetch_json(client, f"{BASE_URL}/regions/local/{province_code}.json")

async def fetch_barangays(client, city_code):
    return await fetch_json(client, f"{BASE_URL}/regions/local/{city_code}.json")

async def fetch_precincts(client, barangay_code):
    prefix = barangay_code[:2]
    return await fetch_json(client, f"{BASE_URL}/regions/precinct/{prefix}/{barangay_code}.json")

async def fetch_precinct_result(client, precinct_code):
    prefix = precinct_code[:3]
    return await fetch_json(client, f"{BASE_URL}/er/{prefix}/{precinct_code}.json")