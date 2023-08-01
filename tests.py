import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from setting import email, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   driver.get('https://petfriends.skillfactory.ru/login')
   yield driver
   driver.quit()

@pytest.fixture()
def test_my_pets(driver):
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys(email)
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys(password)
   # Добавляем явное ожидание
   button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
   # Добавляем неявное ожидание
   driver.implicitly_wait(10)
   button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Переходим на страницу "Мои питомцы"
   driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()
   # Задержка, для визуализации теста
   time.sleep(3)
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.CSS_SELECTOR, 'html > body > nav > a').text == "PetFriends"

def test_quantity_pets(driver, test_my_pets):
   table = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))
   names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   #Берём статистику из личного кабинета
   statistics = driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
   #Берём текст из нулевого элемента статистики
   count_names = statistics[0].text.split('\n')
   #Берем первый элемент из текста
   count_names = count_names[1].split(' ')
   #Присваиваем числовой формат для первого элемента
   count_names = int(count_names[1])
   for i in range(len(names)):
      assert len(names) == count_names
   print('\n', 'Количество питомцев в статистике: ', count_names)
   print('Количество питомцев в таблице: ', len(names))

def test_quantity_pets_with_photo(driver, test_my_pets):
   names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
   # Объявляем переменную - счетчик фотографий
   counter_of_images = 0
   for i in range(len(names)):
      if images[i].get_attribute('src') != '':
          counter_of_images = counter_of_images + 1
   print('\n', 'Количество питомцев c фотографией: ', counter_of_images)
   print('Половина от количества питомцев: ', len(names) / 2)
   assert counter_of_images == (len(names) / 2)


def test_exist_name_age_breed_for_all_my_pets(driver, test_my_pets):
   names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   for i in range(len(names)):
      assert names[i].text != ''
      parts = (names[i].text.split(" "))
      assert len(parts) == 3

def test_all_my_pets_have_different_name(driver, test_my_pets):
   names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   common = []
   elements = []
   duplicate_names = []
   for i in range(len(names)):
      assert names[i].text != ''
      parts = (names[i].text.split(" "))
      common.append(parts)
   print(common)
   for item in common:
      elements.append(item[0])
   for item in elements:
      if elements.count(item) > 1 and item not in duplicate_names:
         duplicate_names.append(item)
   print('\n', 'Питомцы с повторяющемся именем: ', '\n', duplicate_names)
   assert duplicate_names == []

def test_all_my_pets_are_unique(driver, test_my_pets):
   names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   common = []
   duplicates = []
   for i in range(len(names)):
      assert names[i].text != ''
      parts = (names[i].text.split(" "))
      common.append(parts)
   for item in common:
      if common.count(item) > 1 and item not in duplicates:
         duplicates.append(item)
   print('\n', 'Повторяющиеся полностью питомцы:', '\n', duplicates)
   assert duplicates == []
