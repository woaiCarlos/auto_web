import time, smtplib, os, threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import subprocess, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class MyService(Service):
    def __init__(self, executable_path: str,
                 port: int = 0, service_args=None,
                 log_path: str = None, env: dict = None):
        super(Service, self).__init__(
            executable_path,
            port,
            service_args,
            log_path,
            env,
            "Please see https://chromedriver.chromium.org/home")
        # self.creationflags = 134217728
        self.creation_flags = 134217728





class web_auto():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')

    root = tk.Tk()

    # btn_quit.driver = driver

    def quit_browser(self):
        # 通过按钮访问driver对象，并关闭浏览器
        result = messagebox.askokcancel("", "是否关闭程序？")
        if result:
            self.driver.quit()
            self.root.destroy()
        else:
            pass

    def start_web(self):
        # 创建ChromeOptions对象
        self.options = webdriver.ChromeOptions()

        # 设置无头模式（无界面模式）
        self.options.add_argument('--headless')

        self.options.add_argument("--disable-blink-features=AutomationControlled")
        # 设置无痕模式
        # options.add_argument('--incognito')
        self.options.add_argument('executable_path=' + self.chromedriver_path)
        # 指定ChromeOptions对象作为参数创建Chrome浏览器驱动程序
        self.driver = webdriver.Chrome(options=self.options, service=MyService(self.chromedriver_path))
        # 最大化窗口（全屏）
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

        # 打开网页
        url = 'https://baokemengwj.tmall.com/shop/view_shop.htm'  # 将此处URL替换为你想要打开的网页
        self.driver.get(url)

        element = self.driver.find_element(By.XPATH, '//*[@id="login-info"]/a[1]')
        element.click()
        print("点击成功")

        # 切换iframe
        try:
            # 切换到 iframe
            self.driver.switch_to.frame("J_loginIframe")
            # 如果没有出现 NoSuchFrameException 异常，则切换成功
            print("切换到 iframe 成功")
            erweima = self.driver.find_element(By.XPATH, '//*[@id="login"]/div[1]/i')
            erweima.click()

        except:
            print("切换到 iframe 失败")

        # 使用 XPath 定位指定区域的元素
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[2]/div/div[1]/div[1]')))
        qr_code = self.driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/div/div[1]/div[1]')

        qr_code.screenshot('login_qrcode.png')
        with open("login_qrcode.png", "rb") as f:
            image_data = f.read()
        time.sleep(2)
        image = tk.PhotoImage(data=image_data)
        login_qrcode_label.config(image=image)
        login_qrcode_label.image = image
        os.remove("login_qrcode.png")

        result = messagebox.askokcancel("", "是否扫码成功？")
        if result:
            # 清空二维码
            login_qrcode_label.pack_forget()
            # driver.switch_to.default_content()
            store_title = self.driver.title
            login_title = self.driver.find_element(By.CLASS_NAME, 'j_UserNick')
            login_title = login_title.get_attribute('title')
            login_lable.config(text='用户' + login_title + ' 登录成功')
            store_lable.config(text='成功进入店铺：' + store_title)
            # 搜索栏搜索
            self.buy()

        else:
            pass

    def run_selenium(self):
        # 创建一个新的线程来执行Selenium的操作
        threading.Thread(target=self.start_web).start()

    def buy(self):
        try:
            with open('config.txt', 'r', encoding='utf-8') as file:
                config_data = file.read()
                # .split()
        except FileExistsError:
            with open('config.txt', 'w+'):
                pass
            config_data = ''
        while True:
            config_string = config_data
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mq"]')))
            sousuo = self.driver.find_element(By.XPATH, '//*[@id="mq"]')
            sousuo.send_keys(config_string)
            # 点击搜索本店按钮
            find_button = self.driver.find_element(By.XPATH, '//*[@id="J_CurrShopBtn"]')
            find_button.click()
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, "baxia-dialog-content")))
                yanzheng = self.driver.find_element(By.ID, "baxia-dialog-content")
                self.driver.switch_to.frame(yanzheng)
                huadong = self.driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
                action_chains = ActionChains(self.driver)
                action_chains.click_and_hold(huadong)
                # 向右滑动元素
                action_chains.move_by_offset(500, 0)  # 根据需要调整滑动的距离
                action_chains.release()
                action_chains.perform()
                self.driver.switch_to.default_content()

            except:
                pass
            # 获取当前窗口句柄
            current_window_handle = self.driver.current_window_handle

            try:
                # 查找所有元素
                print('//*[contains(text(), "{}")]'.format(config_string))
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "{}" )]'.format(config_string))))
                all_elements = self.driver.find_elements(By.XPATH, '//*[contains(text(), "{}")]'.format(config_string))

                all_elements[0].click()
                time.sleep(5)
                break
            except:
                continue
        # 等待新标签页打开，并获取所有窗口句柄
        all_window_handles = self.driver.window_handles
        # 遍历所有窗口句柄，判断是否为当前窗口句柄，如果不是，则切换到该窗口
        for window_handle in all_window_handles:
            if window_handle != current_window_handle:
                self.driver.switch_to.window(window_handle)
                print('标签页切换成功')
                break

        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'立即购买')]")))
        buy_button = self.driver.find_elements(By.XPATH, "//*[contains(text(),'立即购买')]")
        buy_button[0].click()
        # self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'提交订单')]")))
        # submit_button = self.driver.find_elements(By.XPATH, "//*[contains(text(),'提交订单')]")
        # submit_button[0].click()
        # self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div')))
        # buy_qr_code = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div')
        # buy_qr_code.screenshot('支付二维码.png')
        buy_successful.config(text='购买商品:{}成功\n已发送付款码至邮箱\n请尽快支付订单'.format(config_string))
        # self.send_email()

    def send_email(self):
        # 创建多部分消息对象
        msg = MIMEMultipart('related')

        # 创建HTML内容
        html = """
        <html>
          <body>
            <p>请尽快扫码支付！！！！。</p>
            <p><img src="cid:image1" alt="image"></p>
          </body>
        </html>
        """
        text = MIMEText(html, 'html')
        msg.attach(text)

        # 添加图片
        with open('支付二维码.png', 'rb') as f:
            img_data = f.read()
            image = MIMEImage(img_data)
            image.add_header('Content-ID', '<image1>')
            msg.attach(image)

        # 设置邮件主题、发件人和收件人
        msg['Subject'] = '宝可梦店铺商品已下单请尽快付款'
        msg['From'] = 'lovekiki12138@163.com'
        msg['To'] = '1785932045@qq.com'

        # 发送邮件
        smtp_server = 'smtp.163.com'
        smtp_port = 25
        smtp_username = 'lovekiki12138@163.com'
        smtp_password = 'IARDWTCXWLEJMEUS'

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            print('邮件发送成功')
            os.remove('支付二维码.png')
        except Exception as e:
            print('邮件发送失败:', str(e))


if __name__ == '__main__':
    web_auto_instance = web_auto()
    web_auto.root.geometry("400x300")
    web_auto.root.title("截图显示示例")
    btn_capture = tk.Button(web_auto.root, text="点击登录", command=web_auto_instance.run_selenium)
    btn_capture.pack()
    # 创建按钮用于关闭浏览器
    btn_quit = tk.Button(web_auto.root, text="关闭程序", command=web_auto_instance.quit_browser)
    btn_quit.pack()
    # 创建 Label
    login_qrcode_label = tk.Label(web_auto.root)
    login_qrcode_label.pack()
    login_lable = tk.Label(web_auto.root)
    login_lable.pack()
    store_lable = tk.Label(web_auto.root)
    store_lable.pack()
    buy_successful = tk.Label(web_auto.root)
    buy_successful.pack()
    web_auto.root.mainloop()
