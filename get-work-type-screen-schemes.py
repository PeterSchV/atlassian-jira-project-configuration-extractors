import sys
import requests
import csv
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

api_url_endpoint = f"{JIRA_BASE_URL}/rest/api/3/issuetypescreenscheme"

# Set up authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Function to fetch the work type screen schemes
def fetch_work_type_screen_schemes(auth, api_url_endpoint):
    print("Fetching work type screen schemes from Jira Cloud...")
    response = requests.get(api_url_endpoint, auth=auth)
    print(f"Response status code: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to fetch work type screen schemes: {response.status_code} {response.text}")
        return []

    work_type_screen_schemes = response.json().get('values', [])
    print(f"Found {len(work_type_screen_schemes)} work type screen schemes.")

    return [{'name': scheme['name'], 'id': scheme['id']} for scheme in work_type_screen_schemes]

# Write work type screen schemes to CSV
def write_work_type_screen_schemes_to_csv(work_type_screen_schemes):
    print("Writing work type screen schemes to CSV file...")
    with open('output/work_type_screen_schemes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Name', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for scheme in work_type_screen_schemes:
            writer.writerow({'Name': scheme['name'], 'ID': scheme['id']})
    print("Work type screen schemes saved to work_type_screen_schemes.csv")

# ************************************************************************************************************************************************
# Tests below
# ************************************************************************************************************************************************
fetched_work_type_screen_schemes = fetch_work_type_screen_schemes(auth, api_url_endpoint)

if fetched_work_type_screen_schemes:
    write_work_type_screen_schemes_to_csv(fetched_work_type_screen_schemes)