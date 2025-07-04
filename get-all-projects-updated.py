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

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Function to fetch all projects with pagination
def fetch_all_projects(auth):
    projects = []
    start_at = 0
    while True:
        resp = requests.get(
            f"{JIRA_BASE_URL}/rest/api/3/project/search",
            auth=auth,
            params={'expand': 'lead', 'startAt': start_at, 'maxResults': 100}
        )
        if resp.status_code != 200:
            print("Error fetching projects", resp.status_code, resp.text)
            break
        data = resp.json()
        for p in data.get("values", []):
            projects.append({
                'id': p['id'], 'key': p['key'], 'name': p['name'],
                'lead': p.get('lead', {}).get('accountId', 'N/A')
            })
        if data.get('isLast'):
            break
        start_at += 100
    return projects

def attach_scheme_permissions(auth, project, scheme_name, path, json_key):
    pid = project['id']
    resp = requests.get(f"{JIRA_BASE_URL}/rest/api/3/{path}", auth=auth, params={'projectId': pid})
    if resp.status_code == 200:
        project[scheme_name] = resp.json().get(json_key, 'N/A')
    else:
        print(f"Could not fetch {scheme_name} for {pid}: {resp.status_code}")
        project[scheme_name] = 'N/A'

# Generic helper to fetch and attach scheme data
def attach_scheme(auth, project, scheme_name, path, nested_key):
    pid = project['id']
    url = f"{JIRA_BASE_URL}/rest/api/3/{path}"
    resp = requests.get(url, auth=auth, params={'projectId': pid})

    if resp.status_code != 200:
        print(f"Failed to fetch {scheme_name} for project {project['key']} ({pid}): {resp.status_code}")
        project[scheme_name] = 'N/A'
        return

    data = resp.json()
    values = data.get("values", [])

    if not values:
        project[scheme_name] = 'N/A'
        return

    # Look for the matching project ID inside the values list
    for entry in values:
        if pid in entry.get("projectIds", []):
            nested = entry.get(nested_key, {})
            project[scheme_name] = nested.get("name", "N/A")
            return

    project[scheme_name] = 'N/A'  # fallback


# Specialized fetch functions
def fetch_schemes_for_project(auth, project):
    # This one is already a direct project endpoint
    #attach_scheme(auth, project, 'permission_scheme', f"project/{project['id']}/permissionscheme", '')
    attach_scheme_permissions(auth, project, 'permission_scheme', f"project/{project['id']}/permissionscheme", 'name')

    # These follow the common nested structure in a list
    attach_scheme(auth, project, 'issue_type_scheme', "issuetypescheme/project", 'issueTypeScheme')
    attach_scheme(auth, project, 'issue_type_screen_scheme', "issuetypescreenscheme/project", 'issueTypeScreenScheme')
    attach_scheme(auth, project, 'workflow_scheme', "workflowscheme/project", 'workflowScheme')
    attach_scheme(auth, project, 'field_configuration_scheme', "fieldconfigurationscheme/project", 'fieldConfigurationScheme')


# Main function to fetch all projects and their schemes
def main():
    projects = fetch_all_projects(auth)
    for project in projects:
        fetch_schemes_for_project(auth, project)

    with open('output/project_schemes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'key','name','lead',
            'issue_type_scheme','issue_type_screen_scheme',
            'workflow_scheme','permission_scheme','field_configuration_scheme'
        ])
        writer.writeheader()
        writer.writerows(projects)

if __name__ == "__main__":
    main()
