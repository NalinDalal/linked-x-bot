from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()


def init_driver():
    """Initialize and return a Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)
    return driver


def linkedin_login(driver):
    """Log in to LinkedIn using credentials from environment variables."""
    driver.get("https://www.linkedin.com")
    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )

        username.send_keys(os.getenv("LINKEDIN_EMAIL"))
        password.send_keys(os.getenv("LINKEDIN_PASSWORD"))

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Successfully logged in.")
    except TimeoutException:
        print(
            "Error: Unable to locate login elements. Please check the page structure or your internet connection."
        )
        driver.quit()
        exit()


def search_linkedin(driver, tag):
    """Search for the given tag on LinkedIn and return top results."""
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_box.send_keys(tag)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # Adjust based on loading time

        profiles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='search-result__info']")
            )
        )

        results = []
        for profile in profiles[:3]:  # Limit to top 3
            try:
                name = profile.find_element(By.TAG_NAME, "span").text
                link = profile.find_element(By.TAG_NAME, "a").get_attribute("href")
                results.append((name, link))
            except NoSuchElementException:
                print("Warning: Could not extract all profile details.")
        return results
    except TimeoutException:
        print("Error: Search failed or results took too long to load.")
        return []


def send_requests(results, message):
    """Print the message to be sent to each profile."""
    for name, link in results:
        print(f"Send this message to {name}: {message}\nProfile: {link}")


def main():
    driver = init_driver()
    try:
        linkedin_login(driver)
        tag = input("Enter the tag you want to search for: ")
        custom_message = input("Enter your custom message: ")

        results = search_linkedin(driver, tag)
        if results:
            send_requests(results, custom_message)
        else:
            print("No results found.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
