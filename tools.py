import csv
import os
import uuid
from datetime import datetime
import requests
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()

# def create_ticket(incident: str, short_description: str, user_name: str) -> str:
#     """
#     Create a support ticket and store it in a CSV file.

#     Parameters:
#     ----------
#     incident : str
#         The type or title of the incident being reported.
#     short_description : str
#         A brief explanation describing the issue.
#     user_name : str
#         The name of the user who is reporting the incident.

#     Returns:
#     -------
#     str
#         A confirmation message with the generated Ticket ID.
#     """

#     file_name = "./tickets.csv"

#     # Generate unique Ticket ID
#     ticket_id = f"TKT-{uuid.uuid4().hex[:6].upper()}"

#     # Get current timestamp
#     created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Check if file exists
#     file_exists = os.path.isfile(file_name)

#     with open(file_name, mode="a", newline="") as file:
#         writer = csv.writer(file)

#         # Write header if file doesn't exist
#         if not file_exists:
#             writer.writerow(["Ticket_ID", "Incident", "Short_Description", "User_Name", "Created_At"])

#         # Write ticket data
#         writer.writerow([ticket_id, incident, short_description, user_name, created_at])

#     return f"✅ Ticket created successfully! Your Ticket ID is {ticket_id}"


API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")


def create_ticket(incident: str, short_description: str, user_name: str) -> str:
    """
    Create a support ticket using the remote Ticket API.

    Parameters
    ----------
    incident : str
        The title of the issue.
    short_description : str
        Description of the problem.
    user_name : str
        Name of the reporting user.

    Returns
    -------
    str
        Confirmation message with API response.
    """

    payload = {
        "title": incident,
        "description": short_description,
        "reported_by": user_name,      # remove if your API doesn't need this
        "created_at": datetime.now().isoformat()  # optional
    }

    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)

        if response.status_code in (200, 201):
            data = response.json()
            ticket_id = data.get("ticket_id") or data.get("id") or "UNKNOWN"
            return f"✅ Ticket created successfully! Ticket ID: {ticket_id}"

        return f"❌ Ticket creation failed ({response.status_code}): {response.text}"

    except requests.exceptions.RequestException as e:
        return f"🚨 API connection error: {str(e)}"

def root_cause(incident: str, short_description: str) -> str:
    """
    Check whether the given incident exists in the system records.

    Parameters:
    ----------
    incident : str
        The name or type of the incident.
    short_description : str
        A brief explanation of the issue.

    Returns:
    -------
    str
        A message indicating that the incident is not found in the records.

    Example:
    -------
    >>> root_cause("Server Crash", "Unexpected shutdown during peak hours")
    'The incident "Server Crash" is not in our records.'
    """

    return f'The incident "{incident}" is not in our records.'

def resolution(short_description: list) -> str:
    """
    Provide a basic resolution response for a given issue description.

    Parameters:
    ----------
    short_description : list
        A brief explanation of the reported issue.

    Returns:
    -------
    str
        A suggested resolution message based on the issue description.

    Example:
    -------
    >>> resolution("Server is not responding")
    'Please restart the server and check the network connectivity.'
    """

    return f"Resolution steps for the issue: '{short_description}' are under investigation."


    