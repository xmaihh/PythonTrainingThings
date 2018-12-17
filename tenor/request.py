# encoding:utf-8
# set the apikey and limit
import json

from urllib import request

def get_info_post_json_data(url):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = request.Request(url=url, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    return (res.decode('utf-8'))

def get_():
    apikey = "ZKNSNM7OABLE"  # test value

    lmt = 8

    # load the user's anonymous ID from cookies or some other disk storage
    # anon_id = <from db/cookies>

    # ELSE - first time user, grab and store their the anonymous ID
    # r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % apikey)
    #
    #
    # if r.status_code == 200:
    #     anon_id = json.loads(r.content)["anon_id"]
    #     # store in db/cookies for re-use later
    # else:
    #     anon_id = ""
    #
    # # our test search
    # search_term = "smile"

    # get the top 8 GIFs for the search term
    # r = requests.get(
    #     "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" % (search_term, apikey, lmt, anon_id))
    request_url = "https://api.tenor.com/v1/search?q=smile&key=%s&limit=8&anon_id=%s"
    r = get_info_post_json_data(request_url)
    File = open("hello.json", "w")
    File.write(str(r) + "\n")
    File.close()
    print("success ！！")
    # if r.status_code == 200:
    #     # load the GIFs using the urls for the smaller GIF sizes
    #     top_8gifs = json.loads(r.content)
    #     print
    #     top_8gifs
    # else:
    #     top_8gifs = None

    # continue a similar pattern until the user makes a selection or starts a new search.

if __name__ == '__main__':
    get_()