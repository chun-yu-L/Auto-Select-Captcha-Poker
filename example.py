from anti_poker import AntiPoker
from selenium import webdriver
import time

case_url = "https://web.pcc.gov.tw/prkms/urlSelector/common/tpam?pk=NzA1NDQzMjA="
driver = webdriver.Chrome()
driver.get(case_url)

time.sleep(1)

# 初始化物件
anti_poker = AntiPoker(driver)

anti_poker.auto_solve()

time.sleep(5)