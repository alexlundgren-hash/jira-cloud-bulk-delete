import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('JIRA_ADMIN_API_KEY')
ORG_ID = os.getenv('ORGANIZATION_ID')
DIR_ID = os.getenv('DIRECTORY_ID')

INPUT_FILE = 'account_ids.txt'

def delete_users():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    
    # Read account IDs from file
    try:
        with open(INPUT_FILE, 'r') as f:
            account_ids = [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"Error reading file: {e}")
        return
    
    if not account_ids:
        print(f"No account IDs found in {INPUT_FILE}")
        return
    
    print(f"Starting deletion of {len(account_ids)} users...")
    
    deleted_count = 0
    failed_count = 0
    failed_ids = []
    
    for account_id in account_ids:
        url = f'https://api.atlassian.com/admin/v2/orgs/{ORG_ID}/directories/{DIR_ID}/users/{account_id}'
        
        try:
            response = requests.delete(url, headers=headers)
            
            if response.status_code == 204:
                deleted_count += 1
                print(f"✓ Deleted {account_id}")
            elif response.status_code == 404:
                print(f"✗ User not found: {account_id}")
                failed_count += 1
                failed_ids.append(account_id)
            else:
                print(f"✗ Error deleting {account_id}: {response.status_code} - {response.text}")
                failed_count += 1
                failed_ids.append(account_id)
        except Exception as e:
            print(f"✗ Exception deleting {account_id}: {e}")
            failed_count += 1
            failed_ids.append(account_id)
    
    print(f"\nDeletion complete!")
    print(f"Successfully deleted: {deleted_count}")
    print(f"Failed: {failed_count}")
    
    if failed_ids:
        print(f"\nFailed account IDs:")
        for aid in failed_ids:
            print(f"  {aid}")

if __name__ == "__main__":
    delete_users()
