# -*- coding:utf-8 -*-

import os;
import sys;
import urllib;
import requests;
import socket
import time

def CheckArgs():
    if(len(sys.argv) < 3):
        print('Usage: python ImgSearch.py [Keyword] [DownloadDir] [Pages=1] | 可选 [width] [height]');
        return False;
    return True;

def Download(url, filename, dir):
    try:
        filepath = os.path.join(dir, '%s' % filename);
        if not os.path.isfile(filepath):
            socket.setdefaulttimeout(30)
            urllib.request.urlretrieve(url, filepath);
    except(Exception):  
        print(Exception)
        return ;

def bingRequest(param, dir):
    searchurl = 'http://cn.bing.com/images/async'
    searchurl2 = 'http://cn.bing.com/images/search'
    try:
        response = requests.get(searchurl, params=param);
        text = response.text;
    except(ValueError):
        print(ValueError)
    imgurlMatch = 'murl&quot;:&quot;(https?://[^,]+)&quot;'
    ptxt = re.findall(imgurlMatch,text,re.MULTILINE)
    n = len(ptxt)
    for i in range(n):
        filename = os.path.split(ptxt[i])[1]
        print('Downloading from %s' % ptxt[i]);
        Download(ptxt[i], filename, dir);
    
    try:
        response2 = requests.get(searchurl2, params=param);
        text2 = response2.text;
    except(ValueError):
        return;
    imgurlMatch2 = '<a class="thumb" target="_blank" href="(https?://[^,]+)" h='
    ptxt2 = re.findall(imgurlMatch2,text2,re.MULTILINE)
    n2 = len(ptxt2)
    for i in range(n2):
        filename2 = os.path.split(ptxt2[i])[1]
        print('Downloading from %s' % ptxt2[i]);
        Download(ptxt2[i], filename, dir);
        
def Request(param, dir):
    searchurl = 'http://image.baidu.com/search/avatarjson';
    try:
        response = requests.get(searchurl, params=param);
        json = response.json()['imgs'];
    except(ValueError):
        return;

    for i in range(0, len(json)):
        filename = os.path.split(json[i]['objURL'])[1];
        print('Downloading from %s' % json[i]['objURL']);
        Download(json[i]['objURL'], filename, dir);
    
    return ;

def file_count(dirname,filter_types=[]):
     '''Count the files in a directory includes its subfolder's files
        You can set the filter types to count specific types of file'''
     count=0
     filter_is_on=False
     if filter_types!=[]: filter_is_on=True
     for item in os.listdir(dirname):
         abs_item=os.path.join(dirname,item)
         #print item
         if os.path.isdir(abs_item):
             #Iteration for dir
             count+=file_count(abs_item,filter_types)
         elif os.path.isfile(abs_item):
             if filter_is_on:
                 #Get file's extension name
                 extname=os.path.splitext(abs_item)[1]
                 if extname in filter_types:
                     count+=1
             else:
                 count+=1
     return count

def Search():
    params = {
        'tn' : 'resultjsonavatarnew',
        'ie' : 'utf-8',
        'cg' : '',
        'itg' : '',
        'z' : '0',
        'fr' : '',
        'width' : '',
        'height' : '',
        'lm' : '-1',
        'ic' : '0',
        's' : '0',
        'word' : sys.argv[1],
        'st' : '-1',
        'gsm' : '',
        'rn' : '30'
        };
    dirs = sys.argv[2];
    if(os.path.exists(dirs) == False):
        os.mkdir(dirs);
    if(len(sys.argv) == 3):
        pages = 1;
    elif(len(sys.argv) == 4):
        pages = int(sys.argv[3]);
    elif(len(sys.argv) == 5):
        params['width'] = sys.argv[4];
        params['height'] = sys.argv[4];
    elif(len(sys.argv) == 6):
        params['width'] = sys.argv[4];
        params['height'] = sys.argv[5];

    for i in range(0, pages):
        params['pn'] = '%d' % i;
        Request(params, dirs);
    return ;

def apiBingSearch(words, dirs='./bingDownload', pages=100):
    '''
    '''
    # http://cn.bing.com/images/async?async=content&q=tiger&first=350&count=35
    params = {
        'async': 'content',
        'q' : words,
        'first' : '',
#        'count' : count,
        'FORM': 'HDRSC2'
        };
    if(os.path.exists(dirs) == False):
        os.mkdir(dirs);
    for i in range(0, pages):
        params['first'] = '%d' % i*28+10;
        bingRequest(params, dirs);
        print('等待2秒翻页')
        time.sleep(2)
    

def apiSearch(words, dirs='./downloadImages', pages=1, width='', height=''):
    '''
    api接口函数，便于import使用
    words: 搜索图片关键词
    dir:   图片下载路径，默认为当前目录的./downloadImages文件夹
    pages: 搜索结果含多页，设置下载页数，默认为一页
    width: 设置搜索图片的宽，默认为空，即不作要求
    height:设置搜索图片的高，默认为空，即不作要求
    '''
    params = {
        'tn' : 'resultjsonavatarnew',
        'ie' : 'utf-8',
        'cg' : '',
        'itg' : '',
        'z' : '0',
        'fr' : '',
        'width' : width,
        'height' : height,
        'lm' : '-1',
        'ic' : '0',
        's' : '0',
        'word' : words,
        'st' : '-1',
        'gsm' : '',
        'rn' : '30'
        };
        
    if(os.path.exists(dirs) == False):
        os.mkdir(dirs);

    for i in range(0, pages):
        params['pn'] = '%d' % i;
        Request(params, dirs);
    return ;

if __name__ == '__main__':
    if(CheckArgs() == False):
        sys.exit(-1);
    Search();
    print('Total Images:%d' % file_count(sys.argv[2]));
