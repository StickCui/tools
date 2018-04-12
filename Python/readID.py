# encoding:utf-8
# Author: Stick Cui
# Date:   2018/04/13
# Email:  Stick_Cui@163.com
# Copyright © 2018 Stick Cui.
import re, os, argparse, sys
import datetime

if sys.version_info.major == 2:
    import codecs
    open = codecs.open

parser = argparse.ArgumentParser(description='check and read some informations from ID.')
parser.add_argument('-i','--id', type=str, default=None,
                    help='the ID.')
args = parser.parse_args()

with open('area.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

area = dict()
for line in lines:
    x = line.strip().split(' ')
    key, value = x
    area.update({key: value})

ptxt = '^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'

provs = {11:"北京市",12:"天津市",13:"河北省",14:"山西省",15:"内蒙古自治区",21:"辽宁省",22:"吉林省",23:"黑龙江省",31:"上海市",32:"江苏省",33:"浙江省",34:"安徽省",35:"福建省",36:"江西省",37:"山东省",41:"河南省",42:"湖北省",43:"湖南省",44:"广东省",45:"广西壮族自治区",46:"海南省",50:"重庆市",51:"四川省",52:"贵州省",53:"云南省",54:"西藏自治区",61:"陕西省",62:"甘肃省",63:"青海省",64:"宁夏回族自治区",65:"新疆维吾尔自治区",71:"台湾省",81:"香港特别行政区",82:"澳门特别行政区"}

def checkProv(val):
    pattern = '^[1-9][0-9]'
    a = re.match(pattern, val)
    if a is not None:
        val = a.string
        if int(val) in provs.keys():
            return provs[int(val)]
        else:
            return None
    else:
        return None

def checkDate(val):
    pattern = '^(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)$'
    a = re.match(pattern, val)
    if a is not None:
        val = a.string
        year = val[:4]
        month = val[4:6]
        day = val[-2:]
        date_text = year + '-' + month + '-' + day
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return date_text
        except ValueError:
            return None
    else:
        return None

def checkCode(val):
    factor = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2 ] # 2 ** (17-i) % 11
    parity = [ 1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2 ]
    a = re.match(ptxt, val)
    if a is not None:
        val = a.string
        s = 0
        for i in range(17):
            s += int(val[i]) * factor[i]
        if str(parity[s % 11]) == val[17].upper():
            return val
        else:
            return None
    else:
        return None

def checkGender(val):
    if int(val) % 2 == 0:
        return '女'
    else:
        return '男'

def readID(args):
    ids = checkCode(args.id)
    if ids is not None:
        date = checkDate(ids[6:14])
        if date is not None:
            prov = checkProv(ids[:2])
            if prov is not None:
                if int(ids[0]) < 7:
                    if sys.version_info.major == 2:
                        print(checkGender(ids[-2]) + u', '.encode('utf-8') + prov + area[ids[:6]].encode('utf-8') + u', 生日 '.encode('utf-8') + date)
                    else:
                        print(checkGender(ids[-2]) + u', ' + prov + area[ids[:6]] + u', 生日 ' + date)
                else:
                    if sys.version_info.major == 2:
                        print(checkGender(ids[-2]) + u', '.encode('utf-8') + prov + u', 生日 '.encode('utf-8') + date)
                    else:
                        print(checkGender(ids[-2]) + u', ' + prov + u', 生日 ' + date)
            else:
                print('This ID code is not correct in province code.')
        else:
            print('This ID code is not correct in date format.')
    else:
        print('This ID code is not correct in rule.')

if __name__ == '__main__':
    readID(args)
