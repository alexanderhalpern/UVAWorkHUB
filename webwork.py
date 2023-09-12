import requests
from selenium import webdriver
from time import sleep
import json
import os
from bs4 import BeautifulSoup

from dateutil.parser import parse


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


# check if cookies.json exists
# if it does, load cookies
cookies = None
if os.path.isfile("webwork_cookies.json"):
    json_file = open("webwork_cookies.json", "r")
    try:
        cookies = json.load(json_file)
    except:
        cookies = None
    json_file.close()

if cookies != None:
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    res = s.get(
        'https://webwork.its.virginia.edu/webwork2/Fall23-APMA3080/')
    soup = BeautifulSoup(res.text, 'html.parser')
    currentCourses = soup.find('div', class_='courseList--coursesForTerm')
    print(soup.prettify())

    assignment_table = soup.find('tbody')
    assignments = assignment_table.find_all('tr')

    for assignment in assignments:
        # print(assignment.prettify())
        # get second td tag within assignment
        submission = assignment.find_all('td')[1]
        assignment_name = assignment.find('td')
        # print(assignment_name)

        if "late" not in submission.text.lower():
            print(assignment_name.text)
            res = submission.text.split()
            # remove "at"
            try:
                res.remove("at")
            except:
                pass
            for i in range(len(res) - 1):
                first = res[i]
                second = res[i + 1]
                s = first + " " + second
                # print(s)
                if is_date(first) and is_date(second):
                    print("Due", parse(s))
                    break
            print()


else:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    url = 'https://webwork.its.virginia.edu/webwork2/Fall23-APMA3080/'
    driver.get(url)
    # get current url
    cookies = driver.get_cookies()
    print(driver.current_url)
    while driver.current_url != "https://webwork.its.virginia.edu/webwork2/Fall23-APMA3080/":
        sleep(1)
        print(driver.current_url)
        cookies = driver.get_cookies()
        print("waiting")
        pass

    with open("webwork_cookies.json", "w") as f:
        json.dump(cookies, f)

# cookies = [
#     {'domain': '.gradescope.com',
#      'expiry': 1726059268,
#      'httpOnly': False,
#      'name': 'apt.uid',
#      'path': '/',
#      'sameSite': 'Lax',
#      'secure': False,
#      'value': 'AP-1BQVLBSZC216-2-1694523268768-72314786.0.2.8278e68e-2923-499e-a3fe-244f0c3f3079'},
#     {'domain': '.gradescope.com',
#      'expiry': 1694525069,
#      'httpOnly': False,
#      'name': 'apt.sid',
#      'path': '/',
#      'sameSite': 'Lax',
#      'secure': False,
#      'value': 'AP-1BQVLBSZC216-2-1694523268767-32739186'},
#     {'domain': 'www.gradescope.com', 'httpOnly': True, 'name': '_gradescope_session', 'path': '/', 'sameSite': 'None', 'secure': True,
#      'value': 'OHlhZnJ4RU1MOXJTSzBISzgyVFpnVW0wYm1DYkFldzFnUGZ1eG5wUm5jdWIvRTRSSWhlaVkvNnFrR3hYd3NpeW5nSXo1blg2KzV6U21IbFhyRlozem1wdTkwUzJETjRCdnRpeisxSzJQSHViQm4wdjNtVjE1eU1EbjhCQ2FaUnd3cjJwdXVqdGdDVVRjVWNVVFEvMHJ3TTZZTmVPUUR0eVdQVFEyYlJ5bU8wL0ZWN2NuckQvbkpjU09XdWs3MVhJS1BhSjJLaE1hRlRVTlR2R2Q3MGMyMkhDTG5JVklFYVlxV1VJUmNJN29nV0FLYXRyUHROOVozRHBmMHFCa1FXcUhrU0dNTjkrYk05VjZxTWJROHJwNFoxKzUzZy9scDhOOTdGZ2VpUmtrU0NkVXV3L0p1dU1BWlJTWDZ0RnFZZnZqNGdJczFXRXluU2htTG9hNFREdjhLV044cVlVR3N0WHRPQXRDNEd1bG4zVU54OURyaDJycjJMVFpyVnFmazFCcGFJU2wrRWZ4Y2VMS3AzYjR5bVlPZ1FtdVhLSW0xYzVvZk03YzJxNDZzM1VMTDl2STJaK0lXZlI0aUFNZXBxMmhVYStyZTJ4NENySUVGNnJDOG00VXlvemw5QS82QTI5TWlTVENuaUFLSEFwaTQ4ejM0OFNieVkySUhZSm5xYzBDRlZQYzFqSnZmMGdkdnJyMThpemJlK1ZlVzB0MkFOWTc3YU9ZNkFyYXVVPS0tb1pINFY3eUFKc0g0TmJlOFhQWFJMQT09--463dc78ce3b2de3f99f85a633b22d756c7adafeb'}, {'domain': 'www.gradescope.com', 'expiry': 1729083267, 'httpOnly': False, 'name': 'remember_me', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'V1BIaHIvRDZhM0tHYi9PMnhEQlk0UT09LS1RN2Nxb3didGx3eDAxejRWalRGWHRBPT0%3D--e1e3d8670449e5a8b33815ef669d606ab88c2d21'}, {'domain': 'www.gradescope.com', 'httpOnly': True, 'name': 'signed_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'NXFIYlliRzdWczEvRUdPRVJWYXdiTHBLTzJGUmQva1prdkIwSDNVcWlaQT0tLXZIWml1UXA1K2VwWlpSckNMbzNUaUE9PQ%3D%3D--bc58632a717ceba46fefadd3059e631d3d22d46c'}]

# s = requests.Session()
# for cookie in cookies:
#     s.cookies.set(cookie['name'], cookie['value'])

# print(s.get('https://www.gradescope.com/').text)


# while True:
#     sleep(5)
#     # print cookies
#     cookies = driver.get_cookies()
#     print(cookies)
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Connection": "keep-alive",
#     "Host": "www.gradescope.com",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
# }

# # 1. Login
# r = s.get('https://www.gradescope.com/auth/saml/virginia',
#           headers=headers, allow_redirects=True)
# print(r.text)


# r.html.render()
# print(r.html.html)
# r = s.post(
#     'https://shibidp.its.virginia.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2', headers=headers, allow_redirects=True)

# print(r.text)
