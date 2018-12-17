from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os, sys

login_url = 'https://blackboard.cpp.edu/webapps/bb-auth-provider-cas-bb_bb60/execute/casLogin?cmd=login&authProviderId=_164_1&redirectUrl=https%3A%2F%2Fblackboard.cpp.edu%2Fwebapps%2Fportal%2Fframeset.jsp'

url_templates = {
    'course' : 'https://blackboard.cpp.edu/webapps/blackboard/execute/launcher?type=Course&id={id}&url=',
    'grade_center' : 'https://blackboard.cpp.edu/webapps/gradebook/do/instructor/enterGradeCenter?course_id={id}&cvid=fullGC',
    'download_grades' : 'https://blackboard.cpp.edu/webapps/gradebook/do/instructor/downloadGradebook?dispatch=viewDownloadOptions&course_id={id}'}.items()

class Course:
    def __init__(self, description, url):
        parsed_description = description.split()
        parsed_crn = parsed_description[1].split('.')
        parsed_url = urlparse(url)
        query = parsed_url[4]
        parsed_query = parse_qs(query)

        self.department = parsed_description[0]
        self.crn = parsed_crn[0]
        self.section = parsed_crn[1]
        self.name = self.department+" "+self.crn+"."+self.section
        self.semester = parsed_description[2]
        self.id = parsed_query['id'][0]
        self.urls = {k: v.format(id=self.id) for k, v in url_templates}

class WebDriver:
    def __init__(self, headless=True):
        options = Options()
        options.headless = True
        self.driver = Chrome(chrome_options=options)
        self.in_course = False
        self.driver.implicitly_wait(5)
        self.logged_in = False
        self.courses = {}

    def login(self, username, password):
        self.driver.delete_all_cookies()
        self.driver.get(login_url)
        username_element = self.driver.find_element_by_id('username')
        username_element.send_keys(username)
        passwd_element = self.driver.find_element_by_id('password')
        passwd_element.send_keys(password)
        print('Logging in ... ')
        passwd_element.send_keys(Keys.RETURN)
        self.logged_in = True
        print('Succesfully logged in.')
        raw_courses = self.driver.find_element_by_class_name('coursefakeclass')
        raw_courses_list = raw_courses.find_elements_by_xpath('li')
        for raw_course in raw_courses_list:
            raw_link = raw_course.find_element_by_xpath('a')
            description = raw_link.text
            url = raw_link.get_attribute('href')
            course = Course(description, url)
            self.courses[course.name] = course
        print('Succesfully loaded courses.')

    def enter_course(self, course_name):
        course = self.courses[course_name]
        self.driver.get(course.urls['course'])
        self.in_course = True
        name = course.department+' '+course.crn+'.'+course.section
        print('Entered course: ' + name +'.')

    def create_announcement(self, subject, announcement):
        if self.in_course:
            self.driver.find_element_by_xpath('//*[@id="nav"]/li/a').click()
            subject_field = self.driver.find_element_by_xpath('//*[@id="subject"]')
            subject_field.send_keys(subject)
            iframe = self.driver.find_element_by_xpath('//*[@id="messagetext_ifr"]')
            self.driver.switch_to.frame(iframe)
            html_input = self.driver.find_element_by_xpath('html/body')
            html_input.send_keys(announcement)
            self.driver.switch_to.default_content()
            button = self.driver.find_element_by_class_name('submit')
            button.click()
            print('Succesfully created and posted announcement.')

        else:
            print('You are not in any course. Can`t make the announcement.')

    def quit(self):
        self.driver.quit()
