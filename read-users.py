import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('JIRA_ADMIN_API_KEY')
ORG_ID = os.getenv('ORGANIZATION_ID')
DIR_ID = os.getenv('DIRECTORY_ID')

BASE_URL = f'https://api.atlassian.com/admin/v2/orgs/{ORG_ID}/directories/{DIR_ID}/users'
OUTPUT_FILE = 'account_ids.txt'
NAME_PATTERN = os.getenv('NAME_PATTERN')
DOMAINS = os.getenv('EMAIL_DOMAINS')
GROUP_ID = os.getenv('GROUP_ID')


def fetch_and_filter_users():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    
    # We'll track the cursor manually
    current_cursor = None
    account_ids = set()
    total_users_processed = 0

    print("Starting data retrieval...")

    while True:
        params = {
            'limit': 50
        }
        
        # Add optional emailDomains parameter
        if DOMAINS:
            params['emailDomains'] = DOMAINS
        
        # Add optional groupIds parameter
        if GROUP_ID:
            params['groupIds'] = GROUP_ID
        
        # If we have a cursor from the previous page, add it to params
        if current_cursor:
            params['cursor'] = current_cursor

        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        users = data.get('data', [])

        for user in users:
            # Note: Atlassian Admin API uses 'displayName' in many responses
            name = user.get('displayName', user.get('name', ''))
            if NAME_PATTERN is None or re.match(NAME_PATTERN, name):
                account_ids.add(user.get('accountId'))
            total_users_processed += 1

        # Look for the next cursor in links -> next
        # If 'next' exists, it's just the cursor string, not a URL
        next_link = data.get('links', {}).get('next')
        
        if next_link:
            # The API returns the cursor string here
            current_cursor = next_link
            print(f"Fetched {len(users)} users, moving to next page...")
        else:
            # No more pages
            break

    try:
        with open(OUTPUT_FILE, 'w') as f:
            for aid in account_ids:
                if aid:
                    f.write(f"{aid}\n")
        print(f"Done! Processed {total_users_processed} total users, saved {len(account_ids)} matching Account IDs to {OUTPUT_FILE}.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    fetch_and_filter_users()
