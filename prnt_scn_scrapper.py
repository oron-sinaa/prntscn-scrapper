from string import ascii_lowercase
import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup
import requests
import os
import sys
import time

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HOMEPAGE = "https://prnt.sc/"

def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1

if __name__ == "__main__":
    for letter in ascii_lowercase:
        for letter2 in ascii_lowercase:
            val_letter = letter + letter2
            for num in range(0, 10000, 1):
                if len(str(num)) == 1:
                    val_num = '000' + str(num)
                elif len(str(num)) == 2:
                    val_num = '00' + str(num)
                elif len(str(num)) == 3:
                    val_num = '0' + str(num)
                else:
                    val_num = str(num)
                current_pattern = val_letter + val_num
                current_URL = HOMEPAGE + current_pattern
                status = None
                user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; \
                    en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
                headers={'User-Agent':user_agent,} 
                try:
                    request = urllib.request.Request(current_URL,None,headers)
                    response = urllib.request.urlopen(request)
                    status = "Connected (" + str(response.getcode()) + ")"
                    data = response.read().decode()
                except:
                    status = "Error (" + str(response.getcode())  + ")"
                    exit()
                soup = BeautifulSoup(data, "html.parser")
                link = str(soup.find(id="screenshot-image"))
                image_src = link.split(' ')[-1][5:-3]
                f_name = current_pattern + '.' + image_src.split('.')[-1]
                full_path = "E:/prntscn_scrapped/downloaded_images/" + f_name
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', user_agent)]
                urllib.request.install_opener(opener)
                if image_src.startswith('//st'):
                    continue
                else:
                    try:
                        if os.path.isfile(full_path):
                            print('File exists: ', f_name)
                            continue
                        else: 
                            urllib.request.urlretrieve(image_src, full_path)
                            urllib.request.urlcleanup()
                            print(f_name, " downloaded")
                    except:
                        pass
                del current_pattern, soup
                del link, image_src, f_name, opener