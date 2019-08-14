from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def prepare_driver(path="./chromedriver.exe", headless=True):
    """ Initiate the Chrome driver installed in path
    """
    
    options = Options()
    # make the Chrome driver runs in the background
    if headless:
        options.add_argument('-headless')
    options.add_argument("--lang=en-US")
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(path, options=options)
    return driver