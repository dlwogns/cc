from selenium import webdriver

class crawler:
    def __init__(self, domain_list):
        self.domain_list = domain_list
        self.driver = webdriver.Chrome()
        
        
    