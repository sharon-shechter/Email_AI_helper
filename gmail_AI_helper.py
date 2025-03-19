import redis
import json
from gmail_API_service import authenticate, fetch_emails_with_cache
from LLM_email_Processor import process_email_with_llm
from redisCashing import store_emails_in_redis, get_cached_emails
from visualizations import plot_response_requirements

def main():
    requierd_emails = input("Enter the number of emails you want to fetch: ")
    # Step 1: Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # Step 2: Authenticate and fetch emails (from cache or Gmail API)
    service = authenticate('token.json')
    emails_json = fetch_emails_with_cache(service, redis_client, key="emails:primary", max_results=requierd_emails, expiration_seconds=14400)

    # If emails_json is a string, decode it; otherwise, use it as is
    if isinstance(emails_json, str):
        emails = json.loads(emails_json)  # Convert JSON string to Python list
    else:
        emails = emails_json  # It's already a list

    print("Fetched emails:", json.dumps(emails))

    # add a check if the email are akready processed
    processed_emails = get_cached_emails(redis_client, key="processed_emails")
    if processed_emails:
        print("Retrieved processed emails from Redis cache.")
        print("Processed emails:", processed_emails)
        return
    

    # Step 3: Process emails using LLM
    processed_emails = []
    for email in emails:
        processed_email = process_email_with_llm(email)
        processed_emails.append(processed_email)
    
    print("Processed emails:", json.dumps(processed_emails, indent=4))

    # Step 4: Store processed emails in Redis
    processed_emails_json = json.dumps(processed_emails)
    store_emails_in_redis(redis_client, key="processed_emails", emails_json=processed_emails_json)

    # Step 5: Visualization
    plot_response_requirements(processed_emails)

if __name__ == "__main__":
    main()
