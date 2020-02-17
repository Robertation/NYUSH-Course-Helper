# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 14:31:56 2020

@author: yz391
"""

import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

info = {'name':'net ID','password':''}

def rwait():        # regular wait
    time.sleep(0.5)



def crawl(wd,info):      
    
    #login and enter course_search_page
    wd.get("http://albert.nyu.edu/albert_index.html")
    sign_in_bt = wd.find_element(By.XPATH,"//div[@class = 'textBox']/a[position() = 1]")
    sign_in_bt.click()
    name_box = wd.find_element(By.XPATH,"//input[position() = 1]")
    name = info['name']
    for i in range(len(name)):
        name_box.send_keys(name[i])
        time.sleep(0.1)
    password_box = wd.find_element(By.XPATH,"//input[position() = 2]")
    password = info['password']
    for i in range(len(password)):
        password_box.send_keys(password[i])
        time.sleep(0.1)
    rwait()
    login_btn = wd.find_element(By.XPATH,"//button[@type = 'submit']")
    login_btn.click()
    time.sleep(2)
    wd.switch_to.frame("duo_iframe")
    push_btn = wd.find_element(By.XPATH,"//button[position() = 1]")
    push_btn.click()
    wd.switch_to.parent_frame()
    wait = WebDriverWait(wd,60)
    term_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class = 'isSSS_FullW isSSS_ShopCart isSSS_CartByCareer isSSS_noBkBr isSSS_ShCtCarUGRD selected']//a[@id = 'IS_SSS_ShCtTm1204UGRDLnk']")))
    time.sleep(2)
    term_btn.click()
    wait = WebDriverWait(wd,60)
    wait.until(EC.presence_of_element_located((By.XPATH,"//div [@class = 'isSSS_ShCtEmpWrp']//a")))
    course_search_btn = wd.find_elements(By.XPATH,"//div [@class = 'isSSS_ShCtEmpWrp']//a")[1]
    course_search_btn.click()
    search_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@name = 'DERIVED_REGFRM1_SSR_PB_SRCH']")))
    time.sleep(1)
    search_btn.click()
    time.sleep(10)
    
    # generate index --> major dictionary
    index_to_name = dict()
    html = wd.page_source
    tree = etree.HTML(html)
    for i in range(86,105):
        xpath_search_key = "//span[@id = 'LINK1$span${}']/a/text()".format(i)
        index_to_name['1-'+str(i)] = tree.xpath(xpath_search_key)[0]    
    for i in range(82,101):
        xpath_search_key = "//span[@id = 'LINK2$span${}']/a/text()".format(i)
        index_to_name['2-'+str(i)] = tree.xpath(xpath_search_key)[0]        

    
        
    
        
    
    
    # start browsing major list
    job_finished = False
    index = 86              
    link = 1
    while not job_finished:     #span$1 86~100 and span$2 82~105  represents index for NYUSH majors
        
        if index > 104:
            link = 2
            index = 82
            
        major_name = index_to_name[str(link)+'-'+str(index)]
        print('Checking major: ', major_name)
        xpath_search_key = "//span[@id = 'LINK{}$span${}']/a".format(link,index)
        wait = WebDriverWait(wd,60)
        course_title_btn = wait.until(EC.presence_of_element_located((By.XPATH,xpath_search_key)))
        time.sleep(1)
        course_title_btn.click()
        

        #open up learn_more_buttons
        wait = WebDriverWait(wd,40)
        wait.until(EC.presence_of_element_located((By.XPATH,"//a[@title = 'Expand section Click here to learn more:   | Term/s Filter: Spring 2020']")))
        length = len(wd.find_elements(By.XPATH,"//a[@title = 'Expand section Click here to learn more:   | Term/s Filter: Spring 2020']"))
        for i in range(length):
            btn = wd.find_elements(By.XPATH,"//a[@title = 'Expand section Click here to learn more:   | Term/s Filter: Spring 2020' or @title = 'Collapse section Click here to learn more:   | Term/s Filter: Spring 2020']")[i]        
            while True:
                try:
                    btn.click()
                    break
                except:
                    time.sleep(2)
                    btn = wd.find_elements(By.XPATH,"//a[@title = 'Expand section Click here to learn more:   | Term/s Filter: Spring 2020' or @title = 'Collapse section Click here to learn more:   | Term/s Filter: Spring 2020']")[i]
                    print('another click attempt')
            print('打开下标',i)
            wd.switch_to.parent_frame()
            time.sleep(8)

            
        #open up course details
        length = len(wd.find_elements(By.XPATH,"//div[@style = 'display: block;']//a"))
        print('长度：',length)
        for i in range(length):
            try:
                btn = wd.find_elements(By.XPATH,"//div[@style = 'display: block;']//a")[i]
                btn.click()
                print('打开简介',i)
                time.sleep(1)
            except:
                print('index problem')
                
    
        #save source page            
        source = wd.page_source
        file_path = "C:/Users/yz391/Desktop/Course_info/" + major_name + '.html'
        with open(file_path,'w',encoding = 'utf-8') as fs:
            fs.write(source)
            
        
        back_btn = wd.find_element(By.XPATH,"//input[@name = 'NYU_CLS_DERIVED_BACK']")
        back_btn.click()
        time.sleep(8)
        
        index += 1
        
        job_finished = link == 2 and index >100
        
            
            
    
    
    
    
    

def main():
    info = {'name':'yz3919','password':'gJ9w32e!'}
    wd = webdriver.Chrome()
    crawl(wd,info)


if __name__ == "__main__":
    main()






    









