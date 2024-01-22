import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def open_first_youtube_video(search_query):
    # Specify the path to geckodriver
    service = FirefoxService(executable_path='/usr/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    
    # Open YouTube
    driver.get("http://www.youtube.com")

    # Wait for the search box to be ready for input
    wait = WebDriverWait(driver, 20)  # Increased timeout
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
        search_box.send_keys(search_query + Keys.RETURN)
    except TimeoutException:
        print("Search box not found or not clickable.")
        driver.quit()
        return

    # Check if the page has fully loaded
    page_state = driver.execute_script('return document.readyState;')
    if page_state != 'complete':
        time.sleep(3)  # Wait for 3 seconds if the page has not fully loaded

    # Wait for the results to load and for the first video to be clickable
    first_video_xpath = "(//ytd-video-renderer//a[@id='video-title'])[1]"
    for _ in range(3):  # Retry up to 3 times
        try:
            first_video = wait.until(EC.element_to_be_clickable((By.XPATH, first_video_xpath)))
            first_video.click()
            break
        except TimeoutException:
            print("Retrying to find the first video...")
    else:
        print("First video not found or not clickable.")
        driver.quit()
        return

    # ... additional code ...

    # Optionally, close the browser after some time or based on some condition
    # driver.quit()

if __name__ == "__main__":
    open_first_youtube_video("Tony")
