import matplotlib.pyplot as plt
from collections import Counter




def plot_response_requirements(emails):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot Email Categories
    categories = [email['category'] for email in emails]
    category_counts = Counter(categories)
    axs[0].pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%')
    axs[0].set_title('Email Categories')

    # Plot Email Priorities
    priorities = [email['priority'] for email in emails]
    priority_counts = Counter(priorities)
    axs[1].bar(priority_counts.keys(), priority_counts.values())
    axs[1].set_title('Email Priorities')
    axs[1].set_xlabel('Priority')
    axs[1].set_ylabel('Count')

    # Plot Response Requirements
    response_counts = Counter(email['requires_response'] for email in emails)
    axs[2].bar(response_counts.keys(), response_counts.values())
    axs[2].set_title('Emails Requiring Response')
    axs[2].set_xlabel('Requires Response')
    axs[2].set_ylabel('Count')

    plt.tight_layout()
    plt.show()
    response_counts = Counter(email['requires_response'] for email in emails)

    plt.bar(response_counts.keys(), response_counts.values())
    plt.title('Emails Requiring Response')
    plt.xlabel('Requires Response')
    plt.ylabel('Count')
    plt.show()

if __name__ == "__main__":
    sample_emails = [
        {'category': 'Work', 'priority': 'High', 'requires_response': True},
        {'category': 'Personal', 'priority': 'Low', 'requires_response': False},
        {'category': 'Work', 'priority': 'Medium', 'requires_response': True},
        {'category': 'Spam', 'priority': 'Low', 'requires_response': False},
        {'category': 'Work', 'priority': 'High', 'requires_response': True},
        {'category': 'Personal', 'priority': 'Medium', 'requires_response': False},
    ]


    plot_response_requirements(sample_emails)