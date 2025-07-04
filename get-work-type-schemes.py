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

api_url_endpoint = f"{JIRA_BASE_URL}/rest/api/3/issuetypescheme"

# Set up authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Function to fetch the issue type schemes
def fetch_issue_type_schemes(auth, api_url_endpoint):
    print("Fetching issue type schemes from Jira Cloud...")
    response = requests.get(api_url_endpoint, auth=auth)
    print(f"Response status code: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to fetch issue type schemes: {response.status_code} {response.text}")
        return []

    issue_type_schemes = response.json().get('values', [])
    print(f"Found {len(issue_type_schemes)} issue type schemes.")

    return [{'name': scheme['name'], 'id': scheme['id']} for scheme in issue_type_schemes]

# Write issue type schemes to CSV
def write_issue_type_schemes_to_csv(issue_type_schemes):
    print("Writing issue type schemes to CSV file...")
    with open('output/issue_type_schemes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Name', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for scheme in issue_type_schemes:
            writer.writerow({'Name': scheme['name'], 'ID': scheme['id']})
    print("Issue type schemes saved to issue_type_schemes.csv")

# ************************************************************************************************************************************************
# Tests below
# ************************************************************************************************************************************************
fetched_issue_type_schemes = fetch_issue_type_schemes(auth, api_url_endpoint)

if fetched_issue_type_schemes:
    write_issue_type_schemes_to_csv(fetched_issue_type_schemes)