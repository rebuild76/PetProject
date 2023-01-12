import time
from conftest import web_browser, pytest_runtest_makereport
from selenium.webdriver.common.by import By


def test_petfriends(selenium):
    selenium.get('https://petfriends.skillfactory.ru')
    time.sleep(3)

    btn_newuser = selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()
    time.sleep(3)

    btn_exist_acc = selenium.find_element(By.XPATH, "//a[@href=\"/login\"]")
    btn_exist_acc.click()
    time.sleep(3)

    email_field = selenium.find_element(By.ID, 'email')
    email_field.clear()
    email_field.send_keys('kanabis_5@ka.bis')
    time.sleep(1)

    passw_field = selenium.find_element(By.ID, 'pass')
    passw_field.clear()
    passw_field.send_keys('1234567890-')
    time.sleep(1)

    enter_btn = selenium.find_element(By.XPATH, "//button[@type=\"submit\"]")
    enter_btn.click()
    time.sleep(5)
"""
    if selenium.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        selenium.save_screenshot('result_petfriends.png')
    else:
        raise Exception("login error")
"""
assert web_browser.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"


