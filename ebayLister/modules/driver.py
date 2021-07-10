from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuring the driver
def createDriver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("version='87.0.4280.88'")
    chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9014')
    driver = webdriver.Chrome(options=chrome_options)
    return driver