# encoding:utf-8
# Author: Stick Cui
# Date:   2018/04/11
# Email:  Stick_Cui@163.com
# Copyright © 2018 Stick Cui.

import requests
import re, os, argparse, sys
import time

if sys.version_info.major == 2:
    import codecs
    open = codecs.open

parser = argparse.ArgumentParser(description='Spider for news.')
parser.add_argument('-u','--url', type=str, default='http://www.chinanews.com/scroll-news/{year:d}/{month:02d}{day:02d}/news.shtml',
                    help='the url for getting news.')
parser.add_argument('-s','--start', type=int, default=None,
                    help='the start of the year.')
parser.add_argument('-e','--end', type=int, default=None,
                    help='the end of the year.')
parser.add_argument('-w','--waittime', type=float, default=0.5,
                    help='the waittime of requests frequency. default is 0.5 seconds.')
parser.add_argument('-d','--dir', type=str, default='news',
                    help='where to save the news files.')
args = parser.parse_args()


class ProgressBar(object):
    def __init__(self, progress_bar_length=20, bar='*'):
        self.progress_bar_length = progress_bar_length
        self.bar = bar

    def show_info(self, day, allDay, index, max_length):
        CLEAR_TO_END = "\033[K"
        UP_ONE_LINE = "\033[F"
        c_p = float(index) / max_length
        star_num = int(c_p * self.progress_bar_length)
        info = 'Days [{:d}/{:d}]: [{:d}/{:d}] [{}{}] {:.2%}\n'.format(
            day, allDay, index, max_length, self.bar * star_num, ' ' * (self.progress_bar_length - star_num), c_p)
        sys.stdout.write(UP_ONE_LINE)
        sys.stdout.write('\r' + CLEAR_TO_END)
        sys.stdout.write(info)


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
               AppleWebKit 537.36 (KHTML, like Gecko) Chrome',\
              'Accept': 'text/html,application/xhtml+xml,application/xml;\
                        q=0.9,image/webp,*/*;q=0.8'}
dayseconds = 86400

def getChinaNews():
    if not os.path.exists(args.dir):
        os.mkdir(args.dir)
    localtime = time.localtime()
    if args.end is None:
        args.end = localtime.tm_year
    if args.start is None:
        args.start = localtime.tm_year - 1
    date = time.localtime()
    # Check the args
    if date.tm_year < args.end:
        raise ValueError('The end of year must earlier than this year now.')
    if args.start >= args.end:
        raise ValueError('The start of year must earlier than The end of year (not equal or later).')
    end_days = (date.tm_year - args.end) * 365
    change_days = (args.end - args.start) * 365
    now_time = time.time()
    progressBar = ProgressBar()
    print()
    for dd in range(change_days):
        date = time.localtime(now_time - dayseconds * dd)
        url = args.url.format(year=date.tm_year, month=date.tm_mon, day=date.tm_mday)
        dirpath = os.path.join(args.dir, '{year:d}{month:02d}{day:02d}'.format(year=date.tm_year, month=date.tm_mon, day=date.tm_mday))
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        res = requests.get(url)
        mtxt = '<div class="dd_bt"><a href="([-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])">(.*)</a>'
        code = re.findall('charset=([\w]+)"', res.text)
        res.encoding = code[0]
        newsList = re.findall(mtxt, res.text, re.MULTILINE)
        for i, news in enumerate(newsList):
            time.sleep(args.waittime)
            newsurl, newstitle = news
            if 'http' not in newsurl:
                newsurl = 'http://www.chinanews.com' + newsurl
            newsres = requests.get(newsurl)
            code = re.findall('charset=([\w]+)"', newsres.text) # get the encode type
            newsres.encoding = code[0]
            ad = re.findall('<table[\w\W]*</table></p>', newsres.text, re.MULTILINE) # get the ads table inserted in news context
            if len(ad) != 0: # if there is ad then remove it.
                newNews = re.findall('([\w\W]*)<table[\w\W]*</table>(</p>[\w\W]*)', newsres.text, re.MULTILINE)
                context = newNews[0][0]+newNews[0][1]
            else:
                context = newsres.text
            newscontext = re.findall('<p>(.*)</p>', context, re.MULTILINE) # get the context of news
            # Sometimes, there are not complete news, because the nonstandard html scripts.
            addnewscontext = re.findall('<p>(.*)<div', context, re.MULTILINE) # get the last paragraph if exists.
            editname = re.findall('<div class="left_name">(.*)</div>', context, re.MULTILINE) # get the editor name
            newstime = re.findall('<div class="left-t" style=".*">(.*)<img', context, re.MULTILINE) # get the time of news
            if len(newstime) == 0:
                # All image news, now only get the first page caption.
                newscontext = re.findall('<div class="t3">([\w\W]*)<br></div>', context, re.MULTILINE)
                newstime = ''
            else: # normal news
                if 'href' in newstime[0]: # refine the source of news
                    txt_1 = re.findall('<a .*>(.*)</a>', newstime[0])
                    txt_2 = re.findall('(.*)<a .*>.*</a>', newstime[0])
                    newstime = txt_2[0] + txt_1[0]
                else:
                    newstime = newstime[0]
            with open(os.path.join(dirpath,'20170506_{:03d}.txt'.format(i)), 'w', encoding='utf-8') as f:
                f.writelines(newstitle+'\n'+newstime+'\n')
                for j, par in enumerate(newscontext):
                    if 'href' in par: # refine the first paragraph
                        if j < 3:
                            txt_1 = re.findall('<a .*>(.*)</a>', par)
                            txt_2 = re.findall('<a .*>.*</a>(.*)', par)
                            par = txt_1[0] + txt_2[0]
                        else:
                            continue
                    f.writelines(par + '\n')
                if len(addnewscontext) != 0:
                    for j, par in enumerate(addnewscontext):
                        f.writelines(par + '\n')
                if len(editname) != 0:
                    f.writelines(editname[0] + '\n')
            progressBar.show_info(dd + 1, change_days, i + 1, len(newsList))

def getNews():
    # mtxt = '<a target="_blank" href="(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]+)">([\w^\n]+)</a></li>'
    raise NotImplementedError('Not implemented yet.')

if __name__ == '__main__':
    if 'chinanews' in args.url:
        getChinaNews()
    else:
        getNews()
