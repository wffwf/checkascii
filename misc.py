#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
# import time
import pandas as pd
from string_operator_module import *

'''
def pure_numbers_to_ascii(input_str):
    print("the input_str string  is %s"%input_str)
    input_strs = sort_asc(input_str)
    for i in input_strs:
        if i not in string.digits:
            print("the characters in [input_strs] string is not pure numbers with %s"%sort_asc(input_str))
            return
    try:
        res = [int(i) for i in __import__('re').findall(r'1[0-2][0-9]|[4-9][0-9]', input_str)]
        print("the split number  is",res)
    except:
        print('maybe FAILED in re.findall function')
        return 
    r = bytes(res).decode()
    print("maybe SUCCESS decode result is :",r)

def pure_numbers_to_ascii_by_reverse(input_str):
    pure_numbers_to_ascii(input_str[::-1])

def pure_numbers_to_ascii_function_all(input_str):
    print("---------------------- \033[1;35m[纯数字转ascii字符-正序模式]\033[0m --------------")
    pure_numbers_to_ascii(input_str)
    print("---------------------- \033[1;35m[纯数字转ascii字符-倒序模式]\033[0m --------------")
    pure_numbers_to_ascii_by_reverse(input_str)
def checkfreq(input_str):
    start_time=time.time()
    print("---------------------- \033[1;35m[check character frequency]\033[0m --------------")
    resoult={}
    for i in input_str:
        resoult[i]=input_str.count(i)
    #print(resoult)
    counter_list = sorted(resoult.items(),key=lambda x: x[1],reverse=True)
    print(counter_list)
    r = ''
    for j in counter_list:
        r += j[0]
    print(r)
    print("checkfreq func cost %d seconds"%int(time.time()-start_time))
'''

def checkfreqbypandas(str):
    # print("---------------------- \033[1;35m[按词频排序check character frequency by pandas function]\033[0m --------------")
    print("-"*20+color_string("[按词频排序check character frequency by pandas function]",PURPLE)+"-"*20)    

    list_a = list(str)
    se = pd.Series(list_a)
    resoult = dict(se.value_counts())
    counter_list = sorted(resoult.items(),key=lambda x: x[1],reverse=True)
    print(counter_list)
    r = ''
    for j in counter_list:
        r += j[0]
    print(color_string(r,GREEN))

if __name__ == "__main__":
    c=open('chars_tongji.txt','r').read()
    checkfreqbypandas(c)    