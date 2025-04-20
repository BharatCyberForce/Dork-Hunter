from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import random
from colorama import Fore
from selenium.webdriver.firefox.service import Service

def captcha(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        )
        iframe = driver.find_element('xpath', "//iframe[@title='reCAPTCHA']")  
        driver.switch_to.frame(iframe)  
        checkbox = driver.find_element('css selector', '.recaptcha-checkbox-border')  
        checkbox.click()
        time.sleep(2)
        return True
    except:
        return False


def scraper(dork, op):
    ua = UserAgent()
    options = Options()
    options.set_preference("general.useragent.override", ua.random)
    driver = webdriver.Firefox(options=options)

    try:
        #options = Options()
        options.add_argument("-profile")
        #options.add_argument(r"/home/evil_linux/.mozilla/firefox/3to5its4.default-esr")
        #driver = webdriver.Firefox(service=Service(), options=options)
        driver.get(f"https://www.google.com/")
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.NAME, "q")))

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(dork)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        with open(op, "w") as file:
            #for page in range(1, numb + 1):
            while True:
                driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
                time.sleep(random.uniform(2, 4))

                if captcha(driver):
                    print(Fore.LIGHTRED_EX+"Uff! CaptchA Detected.")

                    input(Fore.GREEN+"Press Enter After Solving The Captcha...")
                    time.sleep(2)

                links = driver.find_elements(By.XPATH, "//a[contains(@href, 'http')]")
                for link in links:
                    href = link.get_attribute("href")
                    if href and "google" not in href:
                        file.write(href + "\n")
                        print(Fore.CYAN+href)
                try:
                    next_button = driver.find_element(By.ID, "pnnext")
                    next_button.click()
                    time.sleep(random.uniform(2, 4))
                except:
                    try:
                        more=driver.find_element(By.XPATH,"//div[contains(@class, 'TOQyFc')]")#//span[contains(@class, 'PBBEhf') and text()='More search results']")))
                        more.click()
                        time.sleep(random.uniform(2, 4))
                    except:
                        print(Fore.LIGHTRED_EX+"Ops! No More Pages Not Found!.")
                        break

    except Exception as e:
        print(Fore.LIGHTRED_EX+f"Error occurred: {e}")
    finally:
        driver.quit()

def banner():
    base=Fore.LIGHTMAGENTA_EX+"""
    ========================================
    |            Dork Hunter Classic       |
    |    Developed by: Indian Cyber Force  |
    ========================================\n\n"""
    print(base)

if __name__ == "__main__":
    banner()
    dork=input(Fore.LIGHTBLUE_EX+"Put Your Dork: ")
    #numb=int(input(Fore.LIGHTBLUE_EX+"Enter The Number Of Page: "))
    op=input(Fore.LIGHTBLUE_EX+"Output File Name: ")

    scraper(dork,op)
    print(Fore.GREEN+f"DonE!{op}")
