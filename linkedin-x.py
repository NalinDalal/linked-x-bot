from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os

# Load environment variables for credentials
load_dotenv()


# LinkedIn Automation
def search_linkedin(tag):
    driver = webdriver.Chrome()  # Ensure you have the correct WebDriver installed
    driver.get("https://www.linkedin.com")

    # Log in to LinkedIn
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    username.send_keys(os.getenv("LINKEDIN_EMAIL"))
    password.send_keys(os.getenv("LINKEDIN_PASSWORD"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(3)  # Wait for login to complete

    # Perform search on LinkedIn
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


# X (Twitter) Automation
def search_x(tag):
    driver = webdriver.Chrome()  # Ensure you have the correct WebDriver installed
    driver.get("https://x.com/login")  # Navigate to X login page

    # Log in to X with WebDriverWait to ensure elements are loaded
    try:
        # Wait until the username field is available
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username.send_keys(
            os.getenv("X_EMAIL")
        )  # Replace with your email in the .env file
        username.send_keys(Keys.RETURN)

        # Wait for the password field to appear
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password.send_keys(
            os.getenv("X_PASSWORD")
        )  # Replace with your password in the .env file
        password.send_keys(Keys.RETURN)

        # Wait for the login to complete and the home page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@aria-label='Timeline: Your Home Timeline']")
            )
        )

    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        return []

    # Perform search on X
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@aria-label='Search query']")
        )
    )
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


# Function to send requests/messages on LinkedIn
def send_linkedin_requests(results, message):
    for name, link in results:
        print(f"Send this message to {name}: {message}\nProfile: {link}")


# Function to send messages on X
def send_x_messages(results, message):
    for username, content in results:
        print(f"Send this message to @{username}: {message}\nTweet Content: {content}")


if __name__ == "__main__":
    platform = (
        input("Which platform would you like to use? (LinkedIn/X): ").strip().lower()
    )
    tag = input("Enter the tag you want to search for: ")
    custom_message = input("Enter your custom message: ")

    if platform == "linkedin":
        results = search_linkedin(tag)
        if results:
            send_linkedin_requests(results, custom_message)
        else:
            print("No results found on LinkedIn.")
    elif platform == "x":
        results = search_x(tag)
        if results:
            send_x_messages(results, custom_message)
        else:
            print("No results found on X.")
    else:
        print("Invalid platform. Please choose either LinkedIn or X.")
