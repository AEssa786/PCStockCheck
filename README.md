PC Stock Checker
A Python-based web scraping application designed to monitor the stock status and prices of PC components across various South African online retailers. This tool helps PC builders track desired parts for their dream build, alerting them to stock availability and potential price drops.

Features
Stock Availability Tracking: Monitors specified PC components on supported websites to check if they are in stock.
Price Monitoring: (Future Enhancement) Will track prices of components and notify you of price changes or drops.
Discord Notifications: Sends updates directly to a Discord channel via a webhook, keeping you informed without manually checking websites.
Containerized (Docker): Runs reliably in a Docker container, making it easy to deploy in environments like GitHub Actions for automated, scheduled checks.
Undetected Chromedriver: Utilizes undetected_chromedriver to minimize detection by anti-bot measures, ensuring consistent scraping.
How it Works
The PC Stock Checker uses Selenium with undetected_chromedriver to navigate to product pages on e-commerce websites. It then extracts stock status and (in future versions) pricing information using BeautifulSoup. All gathered information is compiled into a message and sent to a specified Discord webhook.

The application is designed to run within a Docker container, which allows for consistent execution across different environments. When triggered (e.g., by a GitHub Actions workflow), it builds and runs the container, performs the checks, and sends the notification.

Setup and Installation
To get this program running, you'll need Docker installed on your system.

1. Clone the Repository
First, clone this GitHub repository to your local machine:

Bash

git clone https://github.com/your-username/PCStockChecker.git
cd PCStockChecker
(Remember to replace your-username with your actual GitHub username).

2. Configure Discord Webhook
The program sends notifications to a Discord channel. You'll need to create a Discord Webhook URL:

In your Discord server, go to Server Settings > Integrations > Webhooks > New Webhook.
Give it a name (e.g., "PC Stock Bot") and select the channel where you want notifications to appear.
Copy the Webhook URL. You'll need this URL for the next step.
3. Environment Variables
The Discord Webhook URL needs to be provided as an environment variable.

Locally (for testing):
You can set it in your terminal before running the program:

Bash

export DISCORD_WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL_HERE"
(Replace "YOUR_DISCORD_WEBHOOK_URL_HERE" with the URL you copied).

GitHub Actions (for automated runs):
It's highly recommended to store your Webhook URL as a GitHub Secret for security.

In your GitHub repository, go to Settings > Secrets and variables > Actions > New repository secret.
Name the secret DISCORD_WEBHOOK_URL.
Paste your Discord Webhook URL into the "Secret value" field.
Your GitHub Actions workflow will then automatically pick this up.
4. Build the Docker Image
Navigate to the root directory of the cloned repository (where the Dockerfile is located) and build the Docker image:

Bash

docker build -t stock-checker .
5. Run the Docker Container
Once the image is built, you can run the program:

Bash

docker run --shm-size=2g -e DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL stock-checker
--shm-size=2g: This allocates 2GB of shared memory, which is crucial for Chrome to run smoothly in a containerized environment.
-e DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL: Passes your Discord Webhook URL into the container.
Customization
Adding / Modifying Parts to Track
Edit the evetechParts dictionary in stockTracker.py to change which components are being monitored.

Python

# stockTracker.py
evetechParts = {
    "i5 13600k Processor": "https://www.evetech.co.za/intel-core-i5-13600k-processor/best-deal/16011.aspx",
    "1TB WD Blue SSD": "https://www.evetech.co.za/wd-blue-sn5000-1tb-m2-nvme-ssd/best-deal/22563.aspx",
    # Add more parts here
}
Future: Multi-Website and Price Tracking
As mentioned in the features, the program is designed to be expandable. When adding new websites:

You'll need to identify the correct CSS selectors for stock status and price on each new website. These selectors are unique to each site's HTML structure.
Consider refactoring the evetechParts dictionary into a more flexible data structure to manage multiple URLs and selectors per part.
