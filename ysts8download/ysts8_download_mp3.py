# encoding:utf-8
#
# ysts8_download_mp3
#
# 获取https://www.ysts8.com/有声小说下载
#
# 使用接口文档：
#     INIT = 1                         # index[头] 从第几集到第几集 e.g. 我这里下载<<我当算命先生那些年>> https://www.ysts8.com/Yshtml/Ys16702.html
#     N = 913                          # index[尾]
#     NAME_IN_URL = 'play_16702_55_1'  # 打开正在播放页面的目录名称 e.g. https://www.ysts8.com/play_16702_55_1_2.html   >> play_16702_55_1_2
#
# ==============================================================================
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests


def get():
    INIT = 1  # index[头] 从第几集到第几集 e.g. 我这里下载<<我当算命先生那些年>> https://www.ysts8.com/Yshtml/Ys16702.html
    N = 913  # index[尾]
    NAME_IN_URL = 'play_16702_55_1'  # 打开正在播放页面的目录名称 e.g. https://www.ysts8.com/play_16702_55_1_2.html   >> play_16702_55_1_2

    if not os.path.exists(NAME_IN_URL):
        os.makedirs(NAME_IN_URL)
    os.chdir(NAME_IN_URL)
    head = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36'}
    '''
    html = requests.get(url_s,headers=head)
    with open('a.html','wb') as f:
        f.write(html.content) 
    from bs4 import BeautifulSoup
    bsObj=BeautifulSoup(html.content,'lxml')
    print(bsObj.image)
    '''
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    down_url = ['0'] * (N - INIT + 1)
    i = INIT
    while i <= N:
        url = 'http://www.ysts8.com/' + NAME_IN_URL + '_' + str(i) + '.html'
        driver.get(url)
        driver.switch_to.frame('play')
        source = driver.page_source
        #    with open(str(i+1)+'.html','wt') as f:
        #        f.write(source)
        #    url_str = re.search(r"url[0-9a-zA-Z\_]+ = '(.*)';\n",source)
        #    if url_str:
        #        exec(url_str.group(0))
        #    murl_str = re.search(r"murl[0-9a-zA-Z\_]+ = '(.*)';\n",source)
        #    if murl_str:
        #        exec(murl_str.group(0))
        #    mp3_str = re.search(r"mp3:'(.*)'\n",source)
        #    exec(mp3_str.group(0).replace('mp3:',''))
        #    from selenium.webdriver.support.ui import WebDriverWait
        #    wait = WebDriverWait(driver,10)
        #    wait.until(lambda driver: driver.find_element_by_id('jp_audio_0'))
        try:
            down = driver.find_element_by_id('jp_audio_0')
        except NoSuchElementException:
            #        print('No jp_audio_0 in object ',i,'!')
            continue
        else:
            down_url[i - INIT] = str(down.get_attribute('src'))
            if len(down_url[i - INIT]) > 1:
                print('URL' + str(i) + ': ' + down_url[i - INIT])

                File = open("url.json", "a+")
                File.write('\"url' + str(i) + "\"" + ': \"' + down_url[i - INIT] + "\"" + "\n")
                File.close()

                mp3_down = requests.get(down_url[i - INIT], headers=head)
                # mp3_down.urlretrieve(down_url[i-INIT],str(i)+'.mp3')
                with open(str(i) + '.mp3', 'wb') as f:
                    f.write(mp3_down.content)
                    print('Creat: ' + str(i) + '.mp3!')

                i += 1
    driver.close()

    # for i in range(INIT, N + 1):
    #     mp3_down = requests.get(down_url[i - INIT], headers=head)
    #     # mp3_down.urlretrieve(down_url[i-INIT],str(i)+'.mp3')
    #     with open(str(i) + '.mp3', 'wb') as f:
    #         f.write(mp3_down.content)
    #         print('Creat: ' + str(i) + '.mp3!')


if __name__ == '__main__':
    get()
    # from selenium import webdriver
    #
    # browser = webdriver.Chrome("E:\Python\ysts8download\chromedriver\chromedriver.exe")
