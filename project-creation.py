import os
import requests

# Fetch environment variables with a default value if not set
GITHUB_TOKEN = os.getenv('GH_TOKEN','default_value_if_not_set')
ORG = "sherwin-williams-co"
PROJECT_TITLE = "test_swati_project"

# Check if the critical environment variables are set
if GITHUB_TOKEN == "default_value_if_not_set":
    raise ValueError("The GITHUB_TOKEN environment variable is not set.")
if ORG == "default_org_if_not_set":
    raise ValueError("The ORG environment variable is not set.")
if PROJECT_TITLE == "default_project_title_if_not_set":
    raise ValueError("The PROJECT_TITLE environment variable is not set.")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Step 1: Lookup the org's node_id via REST
org_resp = requests.get(
    f"https://api.github.com/orgs/{ORG}",
    headers=headers
)
org_resp.raise_for_status()
owner_id = org_resp.json()["node_id"]

# Step 2: Create ProjectV2 via GraphQL
graphql_endpoint = "https://api.github.com/graphql"

query = """
mutation($input: CreateProjectV2Input!) {
  createProjectV2(input: $input) {
    projectV2 {
      id
      title
      url
    }
  }
}
"""

variables = {
    "input": {
        "ownerId": owner_id,
        "title": PROJECT_TITLE
    }
}

resp = requests.post(
    graphql_endpoint,
    headers=headers,
    json={"query": query, "variables": variables}
)
resp.raise_for_status()
result = resp.json()

if 'errors' in result:
    raise Exception(result['errors'])

project_url = result["data"]["createProjectV2"]["projectV2"]["url"]
print(f"Created project: {project_url}")
