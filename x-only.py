from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()


def search_x(tag):
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver installed
    driver.get("https://x.com/login")  # Navigate to X login page

    # Log in to X
    time.sleep(2)  # Allow page to load
    username = driver.find_element(By.NAME, "text")
    username.send_keys(os.getenv("X_EMAIL"))  # Replace with your email in the .env file
    username.send_keys(Keys.RETURN)

    time.sleep(2)  # Allow password field to appear
    password = driver.find_element(By.NAME, "password")
    password.send_keys(
        os.getenv("X_PASSWORD")
    )  # Replace with your password in the .env file
    password.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login to complete

    # Perform search
    search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search query']")
    search_box.send_keys(tag)
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for search results to load

    # Extract search results (tweets and usernames)
    results = []
    tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweet']")
    for tweet in tweets[:5]:  # Limit to top 5 results
        try:
            username = tweet.find_element(By.XPATH, ".//div[@dir='ltr']").text
            content = tweet.find_element(By.XPATH, ".//div[@lang]").text
            results.append((username, content))
        except Exception as e:
            print(f"Error extracting tweet: {e}")
            continue

    driver.quit()
    return results


def send_messages(results, message):
    for username, content in results:
        print(f"Send this message to @{username}: {message}\nTweet Content: {content}")


if __name__ == "__main__":
    tag = input("Enter the tag you want to search for: ")
    custom_message = input("Enter your custom message: ")

    results = search_x(tag)
    if results:
        send_messages(results, custom_message)
    else:
        print("No results found.")
