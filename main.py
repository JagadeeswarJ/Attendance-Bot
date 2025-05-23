import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    except Exception as e:
        log(f"Error loading credentials: {e}")
        raise

def initialize_driver(chromedriver_path="chromedriver.exe"):
    log("Initializing headless Chrome WebDriver")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        log("WebDriver initialized successfully")
        return driver
    except Exception as e:
        log(f"Error initializing WebDriver: {e}")
        raise

def login(driver, roll_number, password, url="https://automation.vnrvjiet.ac.in/eduprime3"):
    log(f"Navigating to {url}")
    try:
        driver.get(url)
        
        log("Waiting for username field")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        user_name_element = driver.find_element(By.NAME, "username")
        user_name_element.send_keys(roll_number)
        
        log("Entering password")
        password_element = driver.find_element(By.NAME, "xpassword")
        password_element.send_keys(password, Keys.ENTER)
        
        log("Login attempt completed")
    except Exception as e:
        log(f"Error during login: {e}")
        raise


def navigate_to_attendance(driver):
    log("Navigating to attendance page")
    try:
        log("Waiting for attendance button")
        att_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "attp"))
        )
        att_button.click()
        log("Clicked attendance button")
    except Exception as e:
        log(f"Error navigating to attendance: {e}")
        raise

def extract_attendance(driver, xpath="//h4[@class='font-medium m-b-0']"):
    log("Extracting attendance text")
    try:
        log("Waiting for attendance text element")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        h4_element = driver.find_element(By.XPATH, xpath)
        attendance_text = h4_element.text.strip()
        log(f"Extracted attendance: {attendance_text}")
        return attendance_text
    except Exception as e:
        log(f"Error extracting attendance: {e}")
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

    except Exception as exc:
        # Replace `log` with your own logging or print if needed
        print(f"[ERROR] write_attendance_to_file: {exc}")
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
    except Exception as e:
        log(f"Main application error: {e}")
        raise
    finally:
        if driver:
            log("Waiting for the browser to close manually...")
            try:
                while True:
                    driver.title  # Access a property to check if browser is still alive
                    time.sleep(2)
            except:
                log("Browser closed by user.")
            driver.quit()



if __name__ == "__main__":
    main()