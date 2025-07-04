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

api_url_endpoint = f"{JIRA_BASE_URL}/rest/api/3/workflowscheme"

# Set up authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Function to fetch the workflow schemes
def fetch_workflow_schemes(auth, api_url_endpoint):
    print("Fetching workflow schemes from Jira Cloud...")
    response = requests.get(api_url_endpoint, auth=auth)
    print(f"Response status code: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to fetch workflow schemes: {response.status_code} {response.text}")
        return []

    workflow_schemes = response.json().get('values', [])
    print(f"Found {len(workflow_schemes)} workflow schemes.")

    return [{'name': scheme['name'], 'id': scheme['id']} for scheme in workflow_schemes]

# Write workflow schemes to CSV
def write_workflow_schemes_to_csv(workflow_schemes):
    print("Writing workflow schemes to CSV file...")
    with open('output/workflow_schemes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Name', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for scheme in workflow_schemes:
            writer.writerow({'Name': scheme['name'], 'ID': scheme['id']})
    print("Workflow schemes saved to workflow_schemes.csv")

# ************************************************************************************************************************************************
# Tests below
# ************************************************************************************************************************************************
fetched_workflow_schemes = fetch_workflow_schemes(auth, api_url_endpoint)

if fetched_workflow_schemes:
    write_workflow_schemes_to_csv(fetched_workflow_schemes)