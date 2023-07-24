import os
import platform
import requests
import xml.etree.ElementTree as ET
import zipfile


def get_chrome_version():
    system_name = platform.system()
    if system_name == 'Windows':
        # For Windows
        cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        output = os.popen(cmd).read()
        version = output.split()[-1]
        return version
    elif system_name == 'Darwin':
        # For macOS
        cmd = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'
        output = os.popen(cmd).read()
        version = output.strip().split()[-1]
        return version
    elif system_name == 'Linux':
        # For Linux
        cmd = r'google-chrome --version'
        output = os.popen(cmd).read()
        version = output.strip().split()[-1]
        return version
    else:
        raise Exception("Unsupported operating system")


def version_slice():
    input_string = get_chrome_version()
    index_of_dot = input_string.find('.')
    if index_of_dot != -1:
        result_string = input_string[:index_of_dot + 0]
    else:
        result_string = input_string
    return int(result_string)


def get_chrome_driver():
    response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'.format(version_slice()))
    if str(response) == '<Response [404]>':
        response = requests.get(
            'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'.format(version_slice() - 1))
        version = response.text

    else:
        version = response.text

    chrome_driver = requests.get(
        'https://chromedriver.storage.googleapis.com/?delimiter=/&prefix={}/'.format(version))

    # 解析XML
    root = ET.fromstring(chrome_driver.text)

    # 提取命名空间URI
    namespace_uri = root.tag.split('}')[0][1:]

    # 提取所有下载链接
    namespaces = {'ns': namespace_uri}
    download_links = [item.find('ns:Key', namespaces).text for item in root.findall('.//ns:Contents', namespaces)]

    # 要加在字符串前面的字符
    character_to_prepend = 'https://chromedriver.storage.googleapis.com/'

    # 使用列表推导式在每个字符串前面添加指定字符
    download_links_list = [character_to_prepend + string for string in download_links]

    # 使用列表推导式检查列表中是否包含"linux"的字符串
    system_name = platform.system()
    download_link = ''
    file_name = ''
    if system_name == 'Windows':
        file_name = [url for url in download_links if "win" in url.lower()][0].split('/')[-1]
        download_link = [url for url in download_links_list if "win" in url.lower()][0]
    elif system_name == 'Darwin':
        file_name = [url for url in download_links if "mac64" in url.lower()][0].split('/')[-1]
        download_link = [url for url in download_links_list if "mac64" in url.lower()][0]
    elif system_name == 'Linux':
        file_name = [url for url in download_links if "linux" in url.lower()][0].split('/')[-1]
        download_link = [url for url in download_links_list if "linux" in url.lower()][0]
    response = requests.get(download_link)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.remove(file_name)



get_chrome_driver()