# 🖥️ PCStockCheck

A Python-based stock checker that uses **undetected-chromedriver** and **Selenium** to bypass bot protection and scrape stock status from websites that rely heavily on JavaScript (e.g., Cloudflare-protected sites). Sends Discord alerts when stock is available.

## 🔍 Features

- ✅ Detects stock availability from websites with heavy JavaScript usage
- 🕵️ Bypasses Cloudflare bot protection using `undetected-chromedriver`
- 💬 Sends alerts to a Discord webhook when items are in stock
- 🐳 Easy to deploy with Docker

---

## 📦 Requirements

### Python Packages

The application depends on the following packages:

- `undetected-chromedriver`
- `requests`
- `beautifulsoup4`
- `selenium-stealth`

Install them with:

```bash

pip install -r requirements.txt

```

## 🐳 Docker Setup (Recommended)
Build the Docker image

```bash

docker build -t stock-checker .

```

Run the container
```bash

docker run -e DiscordWebHook="your_webhook_url" stock-checker

```
**💡 Tip: Replace "your_webhook_url" with your actual Discord webhook URL or use a .env file for safer management.**

## 🔧 Configuration
You can edit the stockTracker.py file to target different websites or selectors. By default, the script is set up to:

Load a product page in headless Chrome

Parse the page for stock status text

Send a message to a configured Discord webhook if the item is available

## 🛠️ How It Works
Uses undetected-chromedriver to launch a headless Chrome session

Waits for the page to fully load (to let JavaScript render)

Uses BeautifulSoup and selenium-stealth to parse HTML and mimic human interaction

Sends a POST request to a Discord webhook with stock status

## 🔒 Bypassing Detection
This project uses:

undetected-chromedriver to avoid ChromeDriver detection

selenium-stealth to modify key JavaScript properties and mimic real users

This makes it suitable for scraping websites protected by:

Cloudflare

Bot mitigation services

JavaScript-rendered content

## 📜 License
This project is licensed under the MIT License.

## 🙌 Credits
Built by @AEssa786 with ❤️ to solve the "is it in stock yet?" problem.
