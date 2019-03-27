import urllib.request
from bs4 import BeautifulSoup
from colorama import init, Fore  # init是初始化，Fore是字体颜色


def get():
    init(autoreset=True)  # 初始化
    root_url = 'https://wannianrili.51240.com/'
    response = urllib.request.urlopen(root_url)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')

    tag_soup = soup.find(class_='wnrl_k')
    if tag_soup == None:
        print('Error')
    else:
        print(soup)
        # return;
        detail = tag_soup.find_all(class_='wnrl_k_you')
        for i in range(len(detail)):
            print(detail[i].find(class_='wnrl_k_you_id_biaoti').get_text())
            print(detail[i].find(class_='wnrl_k_you_id_wnrl_nongli').get_text() + '\n')
            tmp = detail[i].find(class_='wnrl_k_you_id_wnrl_jieri_biaoti')
            if(tmp!=None):
                print(Fore.GREEN + detail[i].find(class_='wnrl_k_you_id_wnrl_jieri_biaoti').get_text() )
                print(Fore.WHITE + detail[i].find(class_='wnrl_k_you_id_wnrl_jieri_neirong').get_text() + '\n')
            print(Fore.CYAN + detail[i].find(class_='wnrl_k_you_id_wnrl_yi_biaoti').get_text() + '\r')
            print(Fore.BLUE + detail[i].find(class_='wnrl_k_you_id_wnrl_yi_neirong').get_text() + '\n')
            print(Fore.RED + detail[i].find(class_='wnrl_k_you_id_wnrl_ji_biaoti').get_text() + '\r')
            print(Fore.MAGENTA + detail[i].find(class_='wnrl_k_you_id_wnrl_ji_neirong').get_text() + '\n')
            # print(detail[i].get_text())


if __name__ == '__main__':
    get()
