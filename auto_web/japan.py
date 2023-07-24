import time
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType


def japan_web():
    # 定义ChromeOptions，启用远程调试模式

    chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled --headless")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    # 打开网页
    url = 'https://p-bandai.jp/login/'  # 将此处URL替换为你想要打开的网页
    print('打开网站')
    driver.get(url)
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pbHeader"]/div[1]/div[1]/div[2]/div/ul/li[2]/a')))
    # login = driver.find_element(By.XPATH, '//*[@id="pbHeader"]/div[1]/div[1]/div[2]/div/ul/li[2]/a')
    # login.click()
    login_name = 'Baipiaoluan'
    password = '2shouyigong'
    print('输入账号:{}'.format(login_name))
    print('输入密码:{}'.format(password))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_id"]')))
    login_element = driver.find_element(By.XPATH, '//*[@id="login_id"]')
    login_element.send_keys(login_name)
    password_element = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_element.send_keys(password)
    login_button = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
    login_button.click()

    url1 = 'https://p-bandai.jp/item/item-1000195520/'
    print('查找商品，商品ID：1000195520')
    driver.get(url1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="cdu2mainColumn"]/div[114]/form/div[2]/div[2]/div')))
    gouwuche = driver.find_element(By.XPATH, '//*[@id="buy_side"]')
    gouwuche.click()
    print('加入购物车成功')

    time.sleep(2)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="cdu2mainColumn"]/div[114]/form/div[2]/div[2]/div')))
    cat_gouwuche = driver.find_element(By.XPATH, '//*[@id="cdu2mainColumn"]/div[114]/form/div[2]/div[2]/div/p[1]/a')
    cat_gouwuche.click()
    print('跳转到购物车页面')
    while 1:
        pass


if __name__ == '__main__':
    japan_web()
