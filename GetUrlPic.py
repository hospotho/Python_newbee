from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import requests
import os
import urllib.request

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--disable-web-security')
driver = webdriver.Chrome(chrome_options=chrome_options)
img_folder_path = os.path.dirname(os.path.realpath(__file__))+'\\img\\'
k = 1
if not os.path.exists(img_folder_path):
    os.makedirs(img_folder_path)
else:
    name = []
    for dirPath, dirNames, fileNames in os.walk(img_folder_path):
        for f in fileNames:
            name.append(int(os.path.splitext(f)[0]))
    if name != []:
        k = max(name)+1

url_list = []
img_list = []

try:
    with open('URL.txt', 'r') as f:
        url_list = [line.strip() for line in f]
except:
    pass

u = 1
for url in url_list:
    driver.get(url)
    html = etree.HTML(driver.page_source)
    img_list.extend(html.xpath("//img/@src"))
    print(str(u)+" of "+str(len(url_list))+" done")
    u = u+1

driver.close()

try:
    with open('imgURL.txt', 'r') as f:
        img_list.extend([line.strip() for line in f])
except:
    pass

with open(os.path.dirname(os.path.realpath(__file__))+'\\list.txt', 'w') as f:
        f.writelines(imgURL+'\n' for imgURL in img_list)

count = 1
fail = 0
for img in img_list:
    if img.startswith('http'):
        try:
            file_extension = urllib.request.urlopen(img).info().get_content_subtype()
            r = requests.get(img)
            with open(img_folder_path+str(k)+'.'+file_extension, 'wb') as f:
                f.write(r.content)
            k = k+1
        except:
            fail = fail+1
    print(str(count)+' of '+str(len(img_list))+', failed: '+str(fail))
    count = count+1
