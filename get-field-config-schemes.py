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

api_url_endpoint = f"{JIRA_BASE_URL}/rest/api/3/fieldconfigurationscheme"

# Set up authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Function to fetch the field configuration schemes
def fetch_field_config_schemes(auth, api_url_endpoint):
    print("Fetching field configuration schemes from Jira Cloud...")
    response = requests.get(api_url_endpoint, auth=auth)
    print(f"Response status code: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to fetch field configuration schemes: {response.status_code} {response.text}")
        return []

    field_config_schemes = response.json().get('values', [])
    print(f"Found {len(field_config_schemes)} field configuration schemes.")

    return [{'name': scheme['name'], 'id': scheme['id']} for scheme in field_config_schemes]

# Write field configuration schemes to CSV
def write_field_config_schemes_to_csv(field_config_schemes):
    print("Writing field configuration schemes to CSV file...")
    with open('output/field_config_schemes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Name', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for scheme in field_config_schemes:
            writer.writerow({'Name': scheme['name'], 'ID': scheme['id']})
    print("Field configuration schemes saved to field_config_schemes.csv")

# ************************************************************************************************************************************************
# Tests below
# ************************************************************************************************************************************************
fetched_field_config_schemes = fetch_field_config_schemes(auth, api_url_endpoint)

if fetched_field_config_schemes:
    write_field_config_schemes_to_csv(fetched_field_config_schemes)