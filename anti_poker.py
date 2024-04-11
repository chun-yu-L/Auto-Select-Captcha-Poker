
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import cv2
import numpy as np
import time

class AntiPoker:
    def __init__(self, driver):
        self.driver = driver
        self.result_indices = []
        self.result_images = []

    def get_image(self, XPath):
        img_element = self.driver.find_element(By.XPATH, XPath)
        img = Image.open(io.BytesIO(img_element.screenshot_as_png))

        return img

    def split_image_vertically(self, PIL_image):
        img = PIL_image
        
        # 取得圖片的寬度和高度
        width, height = img.size
        
        # 計算中間位置
        mid_width = width // 2
        
        # 分割圖片
        left_img = img.crop((0, 0, mid_width, height))
        right_img = img.crop((mid_width, 0, width, height))

        split_image_list = [left_img, right_img]
        
        return split_image_list
    
    def get_target_image_list(self):
        XPath = '//*[@id="validateForm"]/table[1]/tbody/tr[1]/td/table/tbody/tr/td[2]/img'
        target_img = self.get_image(XPath)
        target_list = self.split_image_vertically(target_img)

        return target_list
    
    def get_select_image_list(self):
        select_images = []
        for i in range(1, 7):
            Xpath = '//*[@id="validateForm"]/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td[' + str(i) + ']/label/img'
            
            img = self.get_image(Xpath)

            select_images.append(img)

        return select_images

    def calculate_similarity(self, image1, image2):
        # 圖片轉灰階
        gray_image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_BGR2GRAY)

        # 計算相似度
        score = cv2.matchTemplate(gray_image1, gray_image2, cv2.TM_CCOEFF)

        return score[0][0]

    def find_most_similar_images(self, image_list, target_image):
        highest_similarity = -1
        most_similar_images = []
        most_similar_indices = []

        for idx, image in enumerate(image_list):
            similarity = self.calculate_similarity(target_image, image)
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_images = [image]
                most_similar_indices = [idx]
            elif similarity == highest_similarity:
                most_similar_images.append(image)
                most_similar_indices.append(idx)

        return most_similar_images, most_similar_indices

    def solve_poker(self):
        target_list = self.get_target_image_list()
        select_images = self.get_select_image_list()

        self.result_images = []
        self.result_indices = []
        for target_image in target_list:
            similar_images, similar_indices = self.find_most_similar_images(select_images, target_image)
            self.result_images.extend(similar_images[:2])
            self.result_indices.extend(similar_indices[:2])

        return self.result_images, self.result_indices
    
    def click_result(self, result_indices):
        # 點撲克牌
        for idx in result_indices:
            xpath = '//*[@id="validateForm"]/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td[' + str(idx+1) + ']/label/img'
            self.driver.find_element(By.XPATH, xpath).click()
            
    def submit(self):
        self.driver.find_element(By.CSS_SELECTOR, "#b_submit").click()

    def fail_to_solve(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def auto_solve(self):
        while True:
            try:
                self.solve_poker()
                self.click_result(self.result_indices)
                time.sleep(1)
                self.submit()
                time.sleep(1.5)
                
                # 如果解牌失敗，fail_to_solve()才不會報錯
                self.fail_to_solve()
                time.sleep(1.5)
                continue
            
            except:
                break