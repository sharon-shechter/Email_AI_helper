# Gmail AI Helper


## Video 
https://youtu.be/gcgjj3gZyF4


## Overview
The **Gmail AI Helper** is a Python-based tool that connects to a Gmail account using the Gmail API, categorizes emails using a local Large Language Model (LLM), and caches results using Redis. It helps users prioritize their emails based on urgency and importance.

## Features
- **Fetch the latest emails** from your Gmail inbox.
- **Analyze email content** using a local LLM.
- **Categorize emails** into predefined categories (e.g., Work, School, Shopping, etc.).
- **Assign priority levels** (e.g., Urgent, Important, Normal).
- **Determine response necessity** based on email content.
- **Cache results using Redis** for 4 hours to reduce redundant processing.
- **Generate visual insights** using Matplotlib, such as:
  - Pie charts for email categories.
  - Trends over time.
  - Top senders in each category.

## Technologies Used
- **Python**
- **Gmail API** (for email retrieval)
- **Local LLM (GPT4All)** (for email classification)
- **Redis** (for caching email data)
- **Docker** (for running Redis)
- **Matplotlib** (for visualization)


## How It Works
1. Connects to your Gmail using the Gmail API.
2. Fetches the last 100 emails.
3. Calls the local LLM to analyze each email's **subject, sender, and content**.
4. Categorizes and prioritizes emails.
5. Stores results in Redis for faster processing.
6. Generates visual reports.


## License
This project is open-source under the **MIT License**.
