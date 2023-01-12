import time

import pytest
import pytest_check as check
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('/home/user/Selenium/chromedriver')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('kanabis_5@ka.bis')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('1234567890')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # time.sleep(3)

    pytest.driver.find_element(By.CLASS_NAME, "navbar-toggler-icon").click()
    # time.sleep(3)

    pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    # time.sleep(3)

    pets_num = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    if ("Питомцев" in pets_num.text):
        temp = pets_num.text.split(":")
        pets_num = int(temp[1][0:2])
    #1. Find all cards and check with pets_num
    pets_card_num = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
    assert pets_num == len(pets_card_num)

    #2. Half pets have foto
    count_foto_pets = 0
    foto_pets = pytest.driver.find_elements(By.XPATH, '//tr/th/img')
    for i in range(len(foto_pets)):
       if foto_pets[i].get_attribute('src') != '':
          count_foto_pets += 1
    check.less_equal(int(pets_num / 2 + (0.5 if pets_num / 2 > 0 else -0.5)), count_foto_pets)

    #3. Check for name, age not empty
    pet_fields = pytest.driver.find_elements(By.XPATH, '//td')
    for i in range(len(pet_fields)):
        assert pet_fields[i] != ""

    #4. Check for unique names
    temp = []
    for i in range(0, len(pet_fields), 4):
        temp.append(pet_fields[i].text)
    check.equal(len(set(temp)), len(temp), "Есть совпадающие имена! ")

    #5. Check for full duplicate


"""
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   print("\n", len(names))

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0
"""
