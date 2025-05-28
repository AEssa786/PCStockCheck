import undetected_chromedriver as uc
import requests
import bs4
import time
import os
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options # Import Options

evetechParts = {
    "i5 13600k Processor": "https://www.evetech.co.za/intel-core-i5-13600k-processor/best-deal/16011.aspx?srsltid=AfmBOorq3Qw3dCh8MYHqEiBaHDmo0W_jSHIbknzEO4Uv0_390mCf47zL",
    "1TB WD Blue SSD": "https://www.evetech.co.za/wd-blue-sn5000-1tb-m2-nvme-ssd/best-deal/22563.aspx",
    "Corsair RM650 650W Power Supply": "https://www.evetech.co.za/corsair-rm650x-650w-fully-modular-power-supply/best-deal/13189.aspx",
    "MSI PRO B660-A DDR4 Motherboard": "https://www.evetech.co.za/msi-pro-b660-a-ddr4-intel-motherboard/best-deal/18892.aspx",
    "Cooler Master MasterBox K501L Case": "https://www.evetech.co.za/cooler-master-masterbox-k501l-rgb-gaming-case/best-deal/19517.aspx"
}

def checkStock():
    message = ""

    # Initialize Chrome options once outside the loop for efficiency
    # These options are crucial for running headless in Docker
    chrome_options = Options() # Use Selenium's Options for better compatibility
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--no-sandbox") # Required when running as root in Docker
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
    chrome_options.add_argument("--disable-gpu") # Often recommended for headless
    chrome_options.add_argument("--window-size=1920,1080") # Set a consistent window size
    chrome_options.add_argument("--disable-setuid-sandbox") # Good for containers
    chrome_options.add_argument("--disable-extensions") # Disable extensions that might cause issues
    chrome_options.add_argument("--start-maximized") # Maximize window to ensure elements are visible
    chrome_options.add_argument("--single-process") # Sometimes helps with stability in Docker
    # Do NOT set user-agent here if you are using selenium_stealth. Let stealth manage it.
    # If you must set it, make sure it matches the current Chrome version you installed.

    # Initialize the driver once per checkStock call to reduce overhead and potential timeouts
    # This also allows the stealth to be applied once per browser session.
    try:
        driver = uc.Chrome(options=chrome_options,
                            browser_executable_path='/usr/bin/google-chrome-stable', # Path to Chrome installed in Dockerfile
                            driver_executable_path='/usr/local/bin/chromedriver', # Path to ChromeDriver installed in Dockerfile
                            headless=True, # Explicitly tell uc.Chrome to run headless
                            log_level="DEBUG", # Enable debug logs for uc.Chrome
                            )
        # Apply stealth settings
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        driver.implicitly_wait(10) # Set a default implicit wait time for elements
        driver.set_page_load_timeout(60) # Set a timeout for page loading

        for key, value in evetechParts.items():
            try:
                driver.get(value)
                time.sleep(10) # Consider dynamic waits (e.g., WebDriverWait) instead of fixed sleep
                               # Fixed sleeps can be inefficient or insufficient
                html = driver.page_source

                soup = bs4.BeautifulSoup(html, "html.parser")
                stockStatus = soup.select_one("div.py-1.text-\\[16px\\].font-bold")

                if stockStatus: # Simplified check for None
                    message += f"{key}: {stockStatus.text.strip()}\n\n"
                else:
                    message += f"{key}: Stock Status Not Found, Please Check Program or Selector.\n\n"
            except Exception as e:
                message += f"{key}: Error accessing page or finding element: {e}\n\n"
                print(f"Error processing {key} ({value}): {e}") # Print error to logs

    except Exception as e:
        message = f"Error initializing browser: {e}\n\n"
        print(f"Critical error during browser initialization: {e}")
    finally:
        if 'driver' in locals() and driver: # Ensure driver exists before quitting
            driver.quit()

    return message

def sendMessage():
    DiscordWebHook = os.getenv("DISCORD_WEBHOOK_URL") # Ensure this matches your GitHub Secret name
    if not DiscordWebHook:
        print("Error: Discord Webhook URL not found. Please set the DISCORD_WEBHOOK_URL environment variable.")
        return # Exit if webhook URL is not set

    content_message = checkStock()
    try:
        response = requests.post(DiscordWebHook, json={"content": content_message})
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print("Message sent successfully to Discord!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")
        print(f"Response content: {response.text if 'response' in locals() else 'No response'}")


# The script runs sendMessage directly
sendMessage()