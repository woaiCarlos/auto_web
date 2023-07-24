import os
import sys
def hide_chromedriver_console():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')
    print(chromedriver_path)
hide_chromedriver_console()