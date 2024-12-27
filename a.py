from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os

load_dotenv()


def search_linkedin(tag):
    driver = webdriver.Chrome()  # Replace with the appropriate driver for your browser
    driver.get("https://www.linkedin.com")

    # Log in to LinkedIn (replace with your credentials)
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    username.send_keys(os.getenv("LINKEDIN_EMAIL"))
    password.send_keys(os.getenv("LINKEDIN_PASSWORD"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(3)  # Wait for login to complete

    # Perform search
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    search_box.send_keys(tag)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)  # Wait for search results to load

    # Extract top results
    profiles = driver.find_elements(By.XPATH, "//div[@class='search-result__info']")
    results = []
    for profile in profiles[:3]:  # Limit to top 3
        name = profile.find_element(By.TAG_NAME, "span").text
        link = profile.find_element(By.TAG_NAME, "a").get_attribute("href")
        results.append((name, link))

    driver.quit()
    return results


def send_requests(results, message):
    for name, link in results:
        print(f"Send this message to {name}: {message}\nProfile: {link}")


if __name__ == "__main__":
    tag = input("Enter the tag you want to search for: ")
    custom_message = input("Enter your custom message: ")

    results = search_linkedin(tag)
    if results:
        send_requests(results, custom_message)
    else:
        print("No results found.")
