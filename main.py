import schedule
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from courses import security, database, finalproj, database1, security1


#Get current time
now = datetime.now()
courses = {
    "Security": security,
    "Security1": security1,
    "Database": database,
    "Database1": database1,
    "FinalProject": finalproj
}

# Get the day of the week as a string
day_of_week = now.strftime("%A")

# Time of day
current_time = now.hour

#Function to get the info
def get_course_info(course_name):
    course_class = courses.get(course_name)
    return course_class

#First assign course to nothing then change below
course = None

if day_of_week == 'Monday':
    course = get_course_info("Database")
elif day_of_week == 'Tuesday':
    course = get_course_info("Database1")
elif day_of_week == 'Thursday':
    course = get_course_info("FinalProject")
elif day_of_week == 'Friday':
    course = get_course_info("Security")
elif day_of_week == 'Friday' and current_time > 11:
    course = get_course_info("Security1")
else:
    print("Fool, you don't have classes on Wednesdays nor weekends!")
    exit()



browser = webdriver.Chrome()

browser.maximize_window()
browser.get("https://www.gold.ac.uk/students/seats/confirm-attendance/")
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "ccc-notify-accept"))).click()


wait = WebDriverWait(browser, 10)  # Set a 10-second timeout

# Wait for the iframe to be present and store it as a WebElement
iframe_element = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#gecko-form-iframe-embed-21FO00hprjdwl80028mnqwbnpo")))

# Now switch to the iframe using the WebElement
browser.switch_to.frame(iframe_element)

student_id = browser.find_element(By.ID, "form_53171")
student_id.send_keys("33776962")

first_name = browser.find_element(By.ID, "form_53172_first_name")
first_name.send_keys("Joshua")
last_name = browser.find_element(By.ID, "form_53172_last_name")
last_name.send_keys("Ollivierre")

#Get the dropdown wrapper
dropdown_wrapper = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "field58878"))
)

#Select dropdown menu
dropdown = WebDriverWait(dropdown_wrapper, 10).until(
    EC.visibility_of_element_located((By.XPATH, './/div[@ng-switch="field.type"]'))
)
dropdown.click()

#Wait for options to show
options = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, './/ul[contains(@class, "chosen-results")]//li')))

my_option = "Computing"

#Go through the options and click the one that matches my_option
for option in options:
    if option.text == my_option:
        option.click()
        break

module_name= browser.find_element(By.ID, "form_53706")
module_name.send_keys(course.name) #CHANGE THIS LATER TO MAKE IT DYNAMIC BASED ON DAY.

module_code= browser.find_element(By.ID, "form_53705")
module_code.send_keys(course.code) #CHANGE FOR LATER

activity_type= browser.find_element(By.ID, "form_53183")
activity_type.send_keys(course.type) #CHANGE FOR LATER

day = browser.find_element(By.ID, "form_53179_day")
day.send_keys("24")

month= browser.find_element(By.ID, "form_53179_month")
month.send_keys("05")

year= browser.find_element(By.ID, "form_53179_year")
year.send_keys("2434")

session_time = browser.find_element(By.ID, "form_53182")
session_time.send_keys(course.time) #CHANGE

tutor_name = browser.find_element(By.ID, "form_59491")
tutor_name.send_keys(course.lec_name)

room_loc = browser.find_element(By.ID, "form_59492")
room_loc.send_keys(course.room) #CHANGE

reason = browser.find_element(By.ID, "form_53177")
reason.send_keys("Seats not available yet.")

more_than_5 = browser.find_element(By.ID, "form_60221")
more_than_5.send_keys("")

#find the submit button
submit = browser.find_element(By.ID, "form-submit")

try:
    #Waits for the submit button to click
    WebDriverWait(browser, 300).until(
    lambda browser: submit.get_attribute("disabled") == "true" or submit.get_attribute("disabled") == "disabled"
)

    print("Button was clicked and saveHandler() was triggered!")

finally:
    # Switch back to the default content
    browser.switch_to.default_content()
    # Close the browser
    browser.quit()