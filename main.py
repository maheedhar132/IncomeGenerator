from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import yaml
import logging
import os


## Read All the paths from YAML
with open(r"vars.yaml") as file:
    paths = yaml.safe_load(file)

#Headless Browser Options
options = webdriver.ChromeOptions() 
options.add_argument("--headless=new")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#Open the Website
driver.get(paths['siteUrl'])



#Enter Credentials
wait = WebDriverWait(driver, 30)
wait.until(EC.visibility_of_element_located((By.XPATH, paths['usernameBox']))).send_keys(os.getenv('uname'))
wait.until(EC.visibility_of_element_located((By.XPATH, paths['passwdBox']))).send_keys(os.getenv('passwd'))
wait.until(EC.element_to_be_clickable((By.XPATH, paths['loginButton'] ))).click()
time.sleep(5)


Intbalance = float((driver.find_element(By.XPATH, paths['balance'] ).text).replace(",",""))
target = 1.3*Intbalance
print('InitialBalance:',Intbalance)
print('Target for the Day:',target)
loss = 0.4*Intbalance
balance = Intbalance
print('loss:' ,Intbalance - loss)

#Open the Game
wait.until(EC.element_to_be_clickable((By.XPATH, paths['exchangeGame'] ))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, paths['theGame'] ))).click()
time.sleep(30)

def backAntho100():
    logging.info('Started placing Bet')
    wait.until(EC.element_to_be_clickable((By.XPATH, paths['layButton']))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, paths['bet100']))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, paths['placeBets']))).click()
    wait.until(EC.invisibility_of_element_located((By.XPATH, paths['layButton'])))
    balanceVar = float((driver.find_element(By.XPATH, paths['balance'] ).text).replace(",",""))
    if balanceVar <= balance:
        print("betPlaced")


while balance <= target:
    balance = float(((driver.find_element(By.XPATH, paths['balance'] ).text).replace(",","")))
    backAntho100()
    if balance < (Intbalance-loss):
        break

    
