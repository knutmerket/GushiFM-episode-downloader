#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:30:55 2019

@author: knut
"""

import os
import requests
from selenium import webdriver

driver = webdriver.Firefox()

os.makedirs('./GushiFM', exist_ok=True)
os.chdir('./GushiFM')


page_count = 1

episode_list = []

# Get a list of all the episodes
while True:
    driver.get('http://storyfm.cn/episodes/page/' + str(page_count))
    if len(driver.find_elements_by_css_selector("a.soundbyte-podcast-play-progression")) == 0:
        break
    else:
        for i in driver.find_elements_by_css_selector("a.soundbyte-podcast-play-progression"):
            episode_list.append(i.get_attribute('href'))
    page_count += 1
    
print(episode_list)
print("List with a total of %s links from %d pages created" % (len(episode_list), page_count-1))

#Uncomment below lines marked "MP3-URLs" if you want a list of the direct URLs to the MP3s to be printed at the end
#direct_links = [] #MP3-URLs

for link in episode_list:
    driver.get(link)
    try:
        audio_link_raw = driver.find_element_by_css_selector('audio').get_attribute('src')
        # Remove part after ".mp3" from link
        audio_link = audio_link_raw.split('?')[0]
        #direct_links.append(audio_link) #MP3-URLs
        file_name = audio_link.split('/')[-1]
        res = requests.get(audio_link)
        res.raise_for_status()
        save_file = open(file_name, 'wb')
        for chunk in res.iter_content(100000):
            save_file.write(chunk)
    except:
        print('Problem!')
        continue
    
print('All done!')
    
#if len(direct_links) > 0: #MP3-URLs
    #print(direct_links) #MP3-URLs
 