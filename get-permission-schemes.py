import sys
import requests
import csv
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

# What the program does:
# Run API requests to fetch the list of schemes from Jira Cloud and save them to a CSV file. Below are the schemes to fetch:
# - Permission Schemes
# - Issue Type Schemes
# - Workflow Schemes
# - Field Configuration Schemes
# Generate a new CSV file for each scheme type with the scheme name, ID, and if possible, a direct link to it.
# Once all schemes are fetched, move on to fetching the list of projects in Jira Cloud.
# For each project, fetch the associated schemes IDs, and store them in a column to be added to the CSV file.

# Step 1: Set up authentication and headers for the API requests

# Load environment variables from .env file
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

api_url_base = f"{JIRA_BASE_URL}/rest/api/3"
api_url_permissions = f"{api_url_base}/permissionscheme"

# Set up authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Function to fetch the permission schemes
def fetch_permission_schemes(auth, api_url_permissions):
    print("Fetching permission schemes from Jira Cloud...")
    response = requests.get(api_url_permissions, auth=auth)
    print(f"Response status code: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to fetch permission schemes: {response.status_code} {response.text}")
        return []

    permission_schemes = response.json().get('permissionSchemes', [])
    print(f"Found {len(permission_schemes)} permission schemes.")

    return [{'name': scheme['name'], 'id': scheme['id']} for scheme in permission_schemes]

# Write permission schemes to CSV
def write_permission_schemes_to_csv(permission_schemes):
    print("Writing permission schemes to CSV file...")
    with open('output/permission_schemes.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Name', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for scheme in permission_schemes:
            writer.writerow({'Name': scheme['name'], 'ID': scheme['id']})
    print("Permission schemes saved to permission_schemes.csv")

# ************************************************************************************************************************************************
# Tests below
# ************************************************************************************************************************************************
fetched_permission_schemes = fetch_permission_schemes(auth, api_url_permissions)

if fetched_permission_schemes:
    write_permission_schemes_to_csv(fetched_permission_schemes)