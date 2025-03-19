from gpt4all import GPT4All
import json


# Initialize the GPT4All model with the specified file
model_name = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf")


def get_email_category(email):
    """
    Use LLM to classify the email into a category.
    """
    prompt = f"""
    In one word, and simple, determine the category of this email: Work , School, shopping, or Other.
    Please! Don't say anything else; just give the answer.

     Here is an email:
    'Subject: {email['subject']}
    From: {email['from']}
    {email['snippet']}'
    """
    with model_name.chat_session():
        response = model_name.generate(prompt, temp=0.1)
        response = ''.join(e for e in response if e.isalnum() or e.isspace())

   
    return response  




def get_email_priority(email):
    """
    Use LLM to determine the priority of the email.
    """
    prompt = f"""
    In one word, and simple, Determine the priority of the next email with : Urgent, Important, or Normal.
    Please! Don't say anything else; just give the answer.

    Here is an email:
    'Subject: {email['subject']}
    From: {email['from']}
    {email['snippet']}'
    """

    with model_name.chat_session():
        response = model_name.generate(prompt,temp=0.1)
    response = ''.join(e for e in response if e.isalnum() or e.isspace())
    return response.lower()

def check_requires_response(email):
    """
    Use LLM to decide if the email requires a response.
    """
    prompt = f"""
   should i respond to this email?answer with yes or no only.
   and please! Don't say anything else; just give the answer. 

    Here is an email:
    'Subject: {email['subject']}
    From: {email['from']}
    {email['snippet']}'
    """

    with model_name.chat_session():
        response = model_name.generate(prompt,temp=0.1)
    response = ''.join(e for e in response if e.isalnum() or e.isspace())
    return response.lower()

def get_response_message(email):
    """
    Use LLM to generate a polite response message if required.
    """
    prompt = f"""
    please write a polite response to this email.
    just write the response, nothing else.
    start write the email first 

    Here is an email:
    'Subject: {email['subject']}
    From: {email['from']}
    {email['snippet']}'
    """
    with model_name.chat_session():
        response = model_name.generate(prompt,temp=0.1)
    return response

def process_email_with_llm(email):
    """
    Process an email to determine category, priority, response requirement, and response message.
    """
    category = get_email_category(email)
    priority = get_email_priority(email)
    requires_response = check_requires_response(email)
    response_message = get_response_message(email) if requires_response.lower() == "yes" else None

    # Combine results into the email dictionary
    return {
        **email,
        "category": category,
        "priority": priority,
        "requires_response": requires_response,
        "response_message": response_message
    }

if __name__ == "__main__":
    # Example email
    email = {
        "subject": "Meeting Reminder",
        "from": "boss@company.com",
        "snippet": "Don't forget about the meeting tomorrow at 10 AM."
    }

    # Example spam email
    spam_email = {
        "subject": "Congratulations! You've won a prize!",
        "from": "spam@example.com",
        "snippet": "Click here to claim your prize now! This is not a drill, you are a winner!"
    }
    # Example email that requires a response
    response_required_email = {
        "subject": "Project Update Needed",
        "from": "colleague@company.com",
        "snippet": "Can you please provide an update on the project status by end of day?"
    }

  
    # Test individual keys
    # print("Testing Individual Prompts:")
    # print(get_email_category(email))
    # print(get_email_priority(email))
    # print(check_requires_response(spam_email))
    # print(f"Response Message: {get_response_message(email)}")

    # Test full processing
    print("\nTesting Full Processing:")
    processed_email = process_email_with_llm(response_required_email)
    print(json.dumps(processed_email, indent=4))
