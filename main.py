import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import time

def log(message):
    print(f"[DEBUG] {message}")

def load_credentials():
    log("Loading credentials from .env")
    try:
        load_dotenv()
        roll_number = os.getenv("rollNumber")
        password = os.getenv("password")
        if not roll_number or not password:
            raise ValueError("rollNumber or password missing in .env")
        log("Credentials loaded successfully")
        return roll_number, password
    except FileNotFoundError:
        print("[ERROR] .env file not found. Please create a .env file with rollNumber and password.")
        raise
    except ValueError as e:
        print(f"[ERROR] Credential error: {e}")
        print("Please check your .env file contains both 'rollNumber' and 'password' fields.")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error loading credentials: {e}")
        raise

def initialize_driver():
    log("Initializing Chrome WebDriver with automatic driver management")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        log("WebDriver initialized successfully with auto-managed driver")
        return driver
    except Exception as e:
        print(f"[ERROR] Failed to initialize Chrome WebDriver: {e}")
        print("Please ensure Chrome browser is installed and up to date.")
        raise

def login(driver, roll_number, password, url="https://automation.vnrvjiet.ac.in/eduprime3"):
    log(f"Navigating to {url}")
    try:
        driver.get(url)
        
        log("Waiting for username field")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        user_name_element = driver.find_element(By.NAME, "username")
        user_name_element.clear()
        user_name_element.send_keys(roll_number)
        
        log("Entering password")
        password_element = driver.find_element(By.NAME, "xpassword")
        password_element.clear()
        password_element.send_keys(password, Keys.ENTER)
        
        log("Login attempt completed")
        time.sleep(2)  # Wait for login to process
    except TimeoutException:
        print("[ERROR] Login page took too long to load. Check your internet connection.")
        raise
    except NoSuchElementException as e:
        print("[ERROR] Login form elements not found. The website structure may have changed.")
        print(f"Missing element: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        print("Please check your credentials and try again.")
        raise


def navigate_to_attendance(driver):
    log("Navigating to attendance page")
    try:
        log("Waiting for attendance button")
        att_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "attp"))
        )
        att_button.click()
        log("Clicked attendance button")
        time.sleep(2)  # Wait for page to load
    except TimeoutException:
        print("[ERROR] Attendance button not found or not clickable.")
        print("This might be due to:")
        print("  - Login failed (check credentials)")
        print("  - Website structure changed")
        print("  - Network issues")
        raise
    except Exception as e:
        print(f"[ERROR] Failed to navigate to attendance page: {e}")
        raise

def extract_attendance(driver, xpath="//h4[@class='font-medium m-b-0']"):
    log("Extracting attendance text")
    try:
        log("Waiting for attendance text element")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        h4_element = driver.find_element(By.XPATH, xpath)
        attendance_text = h4_element.text.strip()
        
        if not attendance_text:
            raise ValueError("Attendance text is empty")
        
        log(f"Extracted attendance: {attendance_text}")
        return attendance_text
    except TimeoutException:
        print("[ERROR] Attendance data not found on the page.")
        print("This might be due to:")
        print("  - Attendance page didn't load properly")
        print("  - Website structure changed")
        print("  - You might not be on the correct page")
        raise
    except ValueError as e:
        print(f"[ERROR] {e}")
        print("The attendance element was found but contains no data.")
        raise
    except Exception as e:
        print(f"[ERROR] Failed to extract attendance data: {e}")
        raise


def write_attendance_to_file(attendance_text, roll_number, file_path="attendance.csv"):
    """
    Append a roll-number, attendance string, and timestamp to `file_path`.
    Creates the file (with a header row) if it doesn’t exist or is empty.
    """
    try:
        file_exists = os.path.exists(file_path)
        file_empty  = file_exists and os.path.getsize(file_path) == 0

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # local time

        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Add header if the file is new or empty
            if not file_exists or file_empty:
                writer.writerow(["RollNumber", "Attendance", "Timestamp"])

            # Append the new record
            writer.writerow([roll_number, attendance_text, now_str])
        
        log(f"Attendance data written to {file_path}")
        print(f"[SUCCESS] Attendance saved: {attendance_text}")

    except PermissionError:
        print(f"[ERROR] Permission denied writing to {file_path}")
        print("Please ensure the file is not open in another program.")
        raise
    except Exception as exc:
        print(f"[ERROR] Failed to write attendance data: {exc}")
        raise

def main():
    log("Starting main application")
    driver = None
    try:
        roll_number, password = load_credentials()
        driver = initialize_driver()
        login(driver, roll_number, password)
        navigate_to_attendance(driver)
        attendance_text = extract_attendance(driver)
        write_attendance_to_file(attendance_text, roll_number)
        
        print(f"[SUCCESS] Attendance extraction completed for roll number: {roll_number}")
        print("Press any key to close the browser...")
        input()  # Wait for user input before closing
        
    except Exception as e:
        print(f"[ERROR] Application failed: {e}")
        if driver:
            print("Browser will remain open for inspection. Close it manually when done.")
            input("Press any key to exit...")
    finally:
        if driver:
            log("Closing browser")
            driver.quit()



if __name__ == "__main__":
    main()