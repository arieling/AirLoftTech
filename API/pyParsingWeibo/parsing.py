import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree


def start():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    user_id = (int)("2007388957")
    cookie = {
        "Cookie": "_T_WM=a8ce618625235a3d8fde1125f820fca7; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWUjolzr.WehPxhXSBP3ENV5JpX5o2p5NHD95Qf1KnXSK54ehnRWs4DqcjxqPiD9HvjIg4rdsLV9cpDdJMt; gsid_CTandWM=4uDSCpOz5uo3IhLoM7A7qp6Ql1q; M_WEIBOCN_PARAMS=featurecode%3D20000181%26luicode%3D10000011%26lfid%3D1005052007388957; SUB=_2A256jtttDeTxGeNH41YU8CfMwzSIHXVWcOUlrDV6PUJbkdBeLWfWkW2ew1Q9qH-CYyZdROacoaKqSqOZGQ..; SUHB=09P9YK1CmqSmjt; SSOLoginState=1468705597; H5_INDEX=2"}
    url = 'http://weibo.cn/u/%d?filter=1&page=1' % user_id

    html = requests.get(url, cookies=cookie).content
    selector = etree.HTML(html)
    pageNum = (int)("2")

    result = ""
    urllist_set = set()
    word_count = 1
    image_count = 1

    print 'ready to start'

    for page in range(1, pageNum + 1):

        url = 'http://weibo.cn/u/%d?filter=1&page=%d' % (user_id, page)
        lxml = requests.get(url, cookies=cookie).content

        selector = etree.HTML(lxml)
        content = selector.xpath('//span[@class="ctt"]')
        for each in content:
            text = each.xpath('string(.)')
            if word_count >= 4:
                text = "%d :" % (word_count - 3) + text + "\n\n"
            else:
                text = text + "\n\n"
            result = result + text
            word_count += 1

        soup = BeautifulSoup(lxml, "lxml")
        urllist = soup.find_all('a', href=re.compile(r'^http://weibo.cn/mblog/oripic', re.I))
        first = 0
        for imgurl in urllist:
            urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
            image_count += 1

    fo = open("/Users/Arie/airloftweibo/%s" % user_id, "wb")
    fo.write(result)
    word_path = os.getcwd() + '/%d' % user_id
    print 'character finish'

    link = ""
    fo2 = open("/Users/Arie/airloftweibo/%s_imageurls" % user_id, "wb")
    for eachlink in urllist_set:
        link = link + eachlink + "\n"
    fo2.write(link)
    print 'finish image'

    if not urllist_set:
        print 'no image'
    else:
        image_path = '/Users/Arie/airloftweibo/img'
        if os.path.exists(image_path) is False:
            os.mkdir(image_path)
        x = 1
        for imgurl in urllist_set:
            temp = image_path + '/%s.jpg' % x
            print 'picture %s' % x
            try:
                urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(), temp)
            except:
                print "fail:%s" % imgurl
            x += 1

    print 'finish, %d,%s' % (word_count - 4, word_path)
    print 'finish image, %d, %s' % (image_count - 1, image_path)

if __name__ == "__main__":
    start()