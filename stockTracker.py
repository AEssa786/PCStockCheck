import undetected_chromedriver as uc
import requests
import bs4
import time
import os
from selenium_stealth import stealth

evetechParts = {
    "i5 13600k Processor": "https://www.evetech.co.za/intel-core-i5-13600k-processor/best-deal/16011.aspx?srsltid=AfmBOorq3Qw3dCh8MYHqEiBaHDmo0W_jSHIbknzEO4Uv0_390mCf47zL",
    "1TB WD Blue SSD": "https://www.evetech.co.za/wd-blue-sn5000-1tb-m2-nvme-ssd/best-deal/22563.aspx",
    "Corsair RM650 650W Power Supply": "https://www.evetech.co.za/corsair-rm650x-650w-fully-modular-power-supply/best-deal/13189.aspx",
    "MSI PRO B660-A DDR4 Motherboard": "https://www.evetech.co.za/msi-pro-b660-a-ddr4-intel-motherboard/best-deal/18892.aspx",
    "Cooler Master MasterBox K501L Case": "https://www.evetech.co.za/cooler-master-masterbox-k501l-rgb-gaming-case/best-deal/19517.aspx"
}

def checkStock():
    message = ""

    for key, value in evetechParts.items():
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent={}".format(user_agent))

        driver = uc.Chrome(options=chrome_options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        driver.get(value)
        time.sleep(10)
        html = driver.page_source


        soup = bs4.BeautifulSoup(html, "html.parser")
        stockStatus = soup.select_one("div.py-1.text-\\[16px\\].font-bold")

        if(stockStatus != None):
            message += f"{key}: {stockStatus.text.strip()}\n\n"
        else:
            message += f"{key}: Stock Status Not Found, Please Check Program.\n\n"

        driver.quit()

    return message


def sendMessage():
    
    DiscordWebHook = os.getenv("DISCORD_WEBHOOK")
    requests.post(DiscordWebHook, json={"content": checkStock()})


sendMessage()
