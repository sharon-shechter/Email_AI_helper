import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
from bidi.algorithm import get_display  # Import BiDi text processor
from redisCashing import get_cached_emails, store_emails_in_redis


# Authenticate with Gmail API
def authenticate(credentials_file='token.json'):
    """
    Authenticates with the Gmail API using OAuth2 credentials.
    Returns an authenticated service object.
    """
    creds = None
    if os.path.exists(credentials_file):
        creds = Credentials.from_authorized_user_file(credentials_file)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/gmail.readonly']
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(credentials_file, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

# Fetch the last N emails
def fetch_emails(service, max_results=100, query='category:primary'):
    """
    Fetches the last `max_results` emails with their details.
    """
    messages = service.users().messages().list(
        userId='me', maxResults=max_results, q=query
    ).execute().get('messages', [])

    email_list = []
    for index, message in enumerate(messages):
        # Fetch message details directly
        email_id = message['id']
        email = service.users().messages().get(userId='me', id=email_id, format='full').execute()

        # Extract relevant fields
        headers = email.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
        snippet = email.get('snippet', "")

        # Decode and fix text direction
        subject = correct_text_direction(decode_text(subject))
        snippet = correct_text_direction(decode_text(snippet))

        # Append to the list
        email_list.append({
            "id": index + 1,
            "subject": subject,
            "from": sender,
            "snippet": snippet
        })

    return email_list


# decode the text
def decode_text(text):
    """
    Decodes the given text using common encodings.
    Falls back to the original text if decoding fails.
    """
    for encoding in ['utf-8', 'iso-8859-8', 'windows-1255']:
        try:
            return text.encode('latin1').decode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return text  # Return original text if decoding fails


# Correct text direction
def correct_text_direction(text):
    """
    Corrects text direction for RTL languages like Hebrew.
    Uses python-bidi to reorder characters correctly.
    """
    return get_display(text)


# Fetch emails as JSON
def fetch_emails_as_json(service, max_results=100, output_file=None):
    """
    Fetches emails and returns them as a JSON string.
    Optionally saves the JSON to a file.
    """
    emails = fetch_emails(service, max_results)
    emails_json = json.dumps(emails, indent=4, ensure_ascii=False)  # ensure_ascii=False keeps non-ASCII chars readable

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(emails_json)

    return emails_json

def fetch_emails_with_cache(service, redis_client, key="emails:primary", max_results=100, expiration_seconds=14400):
    """
    Fetch emails from cache or Gmail API and store them in Redis.
    """
    # Try to get cached emails
    cached_emails = get_cached_emails(redis_client, key)
    if cached_emails:
        print("Retrieved emails from Redis cache.")
        return cached_emails

    # If not cached, fetch emails from Gmail
    emails_json = fetch_emails_as_json(service, max_results)
    store_emails_in_redis(redis_client, key, emails_json, expiration_seconds)
    print("Fetched emails from Gmail and stored them in Redis.")
    return emails_json


if __name__ == "__main__":
    service = authenticate('token.json')
    emails_json = fetch_emails_as_json(service, max_results=100)

    # Print the JSON
    print(emails_json)

