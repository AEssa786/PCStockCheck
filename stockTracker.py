import undetected_chromedriver as uc
import requests
import bs4
import time
import os
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

evetechParts = {
    "i5 13600k Processor": "https://www.evetech.co.za/intel-core-i5-13600k-processor/best-deal/16011.aspx?srsltid=AfmBOorq3Qw3dCh8MYHqEiBaHDmo0W_jSHIbknzEO4Uv0_390mCf47zL",
    "1TB WD Blue SSD": "https://www.evetech.co.za/wd-blue-sn5000-1tb-m2-nvme-ssd/best-deal/22563.aspx",
    "Corsair RM650 650W Power Supply": "https://www.evetech.co.za/corsair-rm650x-650w-fully-modular-power-supply/best-deal/13189.aspx",
    "MSI PRO B660-A DDR4 Motherboard": "https://www.evetech.co.za/msi-pro-b660-a-ddr4-intel-motherboard/best-deal/18892.aspx",
    "Cooler Master MasterBox K501L Case": "https://www.evetech.co.za/cooler-master-masterbox-k501l-rgb-gaming-case/best-deal/19517.aspx"
}

def checkStock():
    message = ""
    driver = None # Initialize driver to None

    # These options are crucial for running headless in Docker
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--single-process")
    # Added these arguments for more robust headless operation
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--disable-features=NetworkServiceInProcess")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false") # Disable images to save resources
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--proxy-server='direct://'") # No proxy
    chrome_options.add_argument("--proxy-bypass-list=*") # Bypass proxy for all hosts

    try:
        driver = uc.Chrome(options=chrome_options,
                            browser_executable_path='/usr/bin/google-chrome-stable',
                            driver_executable_path='/usr/local/bin/chromedriver',
                            headless=True,
                            )

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)

        for key, value in evetechParts.items():
            try:
                driver.get(value)
                time.sleep(10) # Consider replacing with WebDriverWait for specific elements
                html = driver.page_source

                soup = bs4.BeautifulSoup(html, "html.parser")
                stockStatus = soup.select_one("div.py-1.text-\\[16px\\].font-bold")

                if stockStatus:
                    message += f"{key}: {stockStatus.text.strip()}\n\n"
                else:
                    message += f"{key}: Stock Status Not Found, Please Check Program or Selector.\n\n"
            except Exception as e:
                message += f"{key}: Error accessing page or finding element: {e}\n\n"
                print(f"Error processing {key} ({value}): {e}")

    except Exception as e:
        message = f"Error initializing browser: {e}\n\n"
        print(f"Critical error during browser initialization: {e}")
    finally:
        if driver:
            driver.quit()

    return message

def sendMessage():
    DiscordWebHook = os.getenv("DISCORD_WEBHOOK_URL")
    if not DiscordWebHook:
        print("Error: Discord Webhook URL not found. Please set the DISCORD_WEBHOOK_URL environment variable.")
        return

    content_message = checkStock()
    try:
        response = requests.post(DiscordWebHook, json={"content": content_message})
        response.raise_for_status()
        print("Message sent successfully to Discord!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")
        print(f"Response content: {response.text if 'response' in locals() else 'No response'}")

sendMessage()