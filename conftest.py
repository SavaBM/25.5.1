import pytest
import uuid

from selenium import webdriver


@pytest.fixture(scope = "session")
def driver():
    #global driver
    driver = webdriver.Chrome()

    # Можно задавать нужный вам размер экрана
    # driver.set_window_size(1080, 800)

    # driver.maximize_window()
    return driver
