import urllib.request
import os
import re
from bs4 import BeautifulSoup

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

def get_img(url):
    html = url_open(url)
    bs = BeautifulSoup(html)
    addrs = bs.findAll('p', {'class': 'mh-cover tip'})
    img_addrs = []
    for addr in addrs:
        p = r'url\(([^\)]+[\.jpg|\.png])\)'
        addr = re.findall(p, addr['style'])
        img_addrs.append(addr[0])
    return img_addrs

def get_names(url):
    html = url_open(url).decode('utf-8')
    p = r'a href="/manhua\d+/" title="([^"]+)">[^ ]'
    img_names = re.findall(p, html)
    return img_names

def save_img(folder, img_addrs, img_names):
    for i in range(len(img_names)):
        img_name = img_names[i] + '.' + img_addrs[i].split('.')[-1]
        img_name = img_name.replace(':', '_')
        img_addr = img_addrs[i]
        with open(img_name, 'wb') as f:
            img = url_open(img_addr)
            f.write(img)

def download_comic(folder='comic', pages=1):
    os.mkdir(folder)
    os.chdir(folder)
    url = 'http://www.1kkk.com/manhua-rexue'
    for i in range(pages):
        page_num = i+2
        page_url = url + '-p' +str(page_num)
        img_addrs = get_img(page_url)
        img_names = get_names(page_url)
        save_img(folder, img_addrs, img_names)

winnamedict = [':','|','<','>','*','?','"','/','\\']

if __name__ == '__main__':
    download_comic()
