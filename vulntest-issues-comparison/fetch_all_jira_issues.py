import requests
import json
import os
import http.client as http_client
import logging

# Your Jira credentials and project details
email = "ethan.bui@partior.com"  # Replace with your Jira email
api_token = os.getenv('JIRA_API_KEY')  # Replace with your API token
project_key = "VULNTEST"  # Replace with your Jira project key
domain = "partior.atlassian.net"  # Replace with your Jira domain

# Jira API endpoint for search
url = f"https://{domain}/rest/api/2/search"

# Parameters for the API call
max_results = 100  # Max issues per request
start_at = 0  # Starting index for pagination

# Headers for the request
headers = {
    "Content-Type": "application/json"
}

# Authentication (using email and API token)
auth = (email, api_token)

with open('vulntest_issues_dsc_1187.json', 'w+') as vulntest_issues:
    final_data=[]
    # Loop to handle pagination
    while True:
        print(f'Extracting data from {start_at}')
        # Define the JQL query
        jql_query = f"project = {project_key} and \"Affected Component[Short Text]\" ~ \"image-partior_admin\" ORDER BY cf[10192] DESC"

        # Prepare the request parameters
        params = {
            "jql": jql_query,
            "maxResults": max_results,
            "startAt": start_at,
            "fields": "*all"  # Fetch all fields for the issues
        }

        # Make the GET request to Jira API
        response = requests.get(url, headers=headers, auth=auth, params=params)

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()
            final_data.extend(data["issues"])

            # Check if there are more issues to fetch
            # total = data["total"]
            total = 250
            if start_at + max_results >= total:
                break

            # Increment the startAt value to fetch the next page of issues
            start_at += max_results
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(json.dumps(response.json()))
            break
    vulntest_issues.writelines(json.dumps(final_data))