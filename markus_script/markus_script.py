from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import sys
import getpass

# Set up chrome driver
homepage = 'https://markus.teach.cs.toronto.edu/'
# uw_homepage = 'https://markus.student.cs.uwaterloo.ca/'
path = str(Path(__file__).absolute().parent) + '/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

# Hash table for Course:Link
course_map = dict()

# Sracp the grade of current selected course.
def print_grade ():
    rows = driver.find_elements_by_css_selector('#content .section tr')
    for row in rows:
        col = row.find_elements_by_tag_name('td')
        for data in col:
            data_str = str(data.text)
            data_str = data_str.strip().replace('Results', '').replace('Your mark:', '')
            print(data_str + '\t', end='')
        print()
    print ('\n' + '*' * 40 + '\n')
    return

# Print available courses of current semester.
def print_current_courses ():
    driver.get (homepage)
    course_list = driver.find_elements_by_tag_name('li')
    print ('\n**Available Courses**\n')
    for course in course_list:
        print (course.text)
        course_map [course.find_element_by_tag_name('a').get_attribute('innerHTML').strip().replace(' ', '')] = \
             course.find_element_by_tag_name('a').get_attribute('href')
    print ('\n' + '*' * 40 + '\n')

# Log into the course directory
def log_in ():
    logged_in = False;
    while (not logged_in):
        username = input ('Username: ')
        if (username == 'exit'):
            driver.quit()
            sys.exit()
        password = getpass.getpass('Password: ')
        if (password == 'exit'):
            driver.quit()
            sys.exit()
        print()
        username_input = driver.find_element_by_id('user_login')
        username_input.clear()
        username_input.send_keys(username)
        password_input = driver.find_element_by_id('user_password')
        password_input.clear()
        password_input.send_keys(password)
        submitButton = driver.find_element_by_css_selector('.submit')
        submitButton.click()
        try:
            driver.find_element_by_id('loggedIn')
            logged_in = True
        except:
            logged_in = False
            print('Incorrect Username/Password.')

# Log out after scraping the grades.
def log_out ():
    log_out_button = driver.find_element_by_id('logout_link')
    log_out_button.click()

def main ():
    print_current_courses()
    try:
        while True:
            course = input ('Course# (eg. CSC 373): ').strip().replace(' ', '')
            print()
            if course in course_map:
                driver.get (course_map[course])
                log_in()
                print_grade()
                log_out()
            elif (course == 'exit'):
                driver.quit()
                sys.exit()
            else:
                print ('Course Not Found.')
    finally:
        driver.quit()
