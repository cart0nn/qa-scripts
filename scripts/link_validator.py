import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def validate_links_with_selenium(url):
    try:
        # Configure Selenium WebDriver (for Firefox)
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")  # Run in headless mode, without opening a browser window
        service = GeckoService(executable_path='../pkg/geckodriver.exe', log_path=None)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        # Load the webpage
        driver.get(url)

        # Find all <a> tags
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Validate each link
        results = []
        for link in links:
            href = link.get_attribute('href')
            if href:
                # Check the status of the link (you can continue with the existing validate_link_status function)
                link_status = validate_link_status(href)
                results.append((href, link_status))

        driver.quit()  # Close the WebDriver

        return results

    except Exception as e:
        print(f"Error validating links with Selenium: {e}")
        return []

def validate_link_status(url):
    try:
        # Check the status of the link using requests
        response = requests.head(url, allow_redirects=True)
        status = response.status_code
        if status == 200:
            return "Valid"
        else:
            return f"Invalid (Status Code: {status})"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage:
if __name__ == "__main__":
    url = input("Enter the URL to validate links (with JavaScript content): ").strip()
    
    # Validate links with Selenium and handle results
    validated_links = validate_links_with_selenium(url)

    if validated_links:
        print("\nValidated Links:")
        for link, status in validated_links:
            print(f"{link}: {status}")
    else:
        print("No links found or error occurred.")