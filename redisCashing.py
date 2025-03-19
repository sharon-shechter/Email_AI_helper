import redis
import json

def get_cached_emails(redis_client, key):
    """
    Retrieves cached emails from Redis using the specified key.
    Args:
        redis_client (redis.Redis): The Redis client instance.
        key (str): The key to retrieve cached emails.
    Returns:
        list: Cached emails as a Python list, or None if not found.
    """
    try:
        cached_emails = redis_client.get(key)
        if cached_emails:
            return json.loads(cached_emails)
        else:
            return None
    except Exception as e:
        print(f"Failed to retrieve cached emails: {e}")
        return None

def store_emails_in_redis(redis_client, key, emails_json, expiration_seconds=14400):
    """
    Stores a JSON of emails in Redis with a specified expiration time.
    Args:
        redis_client (redis.Redis): The Redis client instance.
        key (str): The key to store the JSON.
        emails_json (str): The JSON string to store.
        expiration_seconds (int): Expiration time in seconds (default: 4 hours).
    """
    try:
        redis_client.setex(key, expiration_seconds, emails_json)
        print(f"Emails successfully stored in Redis under key: {key}")
    except Exception as e:
        print(f"Failed to store emails in Redis: {e}")

if __name__ == "__main__":
    # Example JSON of emails
    emails_json = json.dumps([
        {"email": "this is a cached email"},
        {"email": "example1@gmail.com"},
        {"email": "example2@gmail.com"}
    ])
    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    store_emails_in_redis(redis_client,"test table", emails_json,10)
    
   
