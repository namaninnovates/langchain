"""Take full-page screenshots of the output HTML using Selenium."""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1200,900")
opts.add_argument("--force-device-scale-factor=2")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)
driver.get("file:///Users/guptanaman/Downloads/langchain/output_screenshots.html")
time.sleep(2)

out_dir = "/Users/guptanaman/Downloads/langchain/screenshots"
import os
os.makedirs(out_dir, exist_ok=True)

# Get full page height
total_height = driver.execute_script("return document.body.scrollHeight")
viewport_height = driver.execute_script("return window.innerHeight")

# Screenshot 1: top of page (Test Cases 1-2)
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/01_test_cases_1_2.png")
print("Saved 01_test_cases_1_2.png")

# Screenshot 2: Test Cases 2-3
driver.execute_script("window.scrollTo(0, 650)")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/02_test_cases_2_3.png")
print("Saved 02_test_cases_2_3.png")

# Screenshot 3: Test Cases 3-4
driver.execute_script("window.scrollTo(0, 1300)")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/03_test_cases_3_4.png")
print("Saved 03_test_cases_3_4.png")

# Screenshot 4: Test Cases 5
driver.execute_script("window.scrollTo(0, 1900)")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/04_test_case_5.png")
print("Saved 04_test_case_5.png")

# Screenshot 5: Test Case 6 Multi-tool (top part)
driver.execute_script("window.scrollTo(0, 2500)")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/05_test_case_6_multi_tool.png")
print("Saved 05_test_case_6_multi_tool.png")

# Screenshot 6: Test Case 6 Multi-tool (response) + Test Case 7
driver.execute_script("window.scrollTo(0, 3200)")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/06_test_case_6_response_and_7.png")
print("Saved 06_test_case_6_response_and_7.png")

# Screenshot 7: Test Case 7 + footer
driver.execute_script(f"window.scrollTo(0, {total_height})")
time.sleep(0.5)
driver.save_screenshot(f"{out_dir}/07_test_case_7_footer.png")
print("Saved 07_test_case_7_footer.png")

driver.quit()
print(f"\nAll screenshots saved to: {out_dir}/")
print(f"Total page height: {total_height}px")
