#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import argparse
import time
import pandas as pd
import numpy as np
import gmpy2
#Imports Necessary Libraries for vigenere
from collections import Counter
import string
import vigenereTools
from yunying import *
from decode_Manchester import *
from decode_Fence import *
from basexx import *
from misc import *
from vigenere_shortest_key_burp import *
from cipin_mix_fangshe_affine import *
from burp_affine import *
from hill_key_burp import *
from vigenere import *
from vigenere_by_dictionary import *
from vigenere_theory_key_burp import* # add at 20250929

def checktxt(input_str):
    # 常见编解码
    checkbasexx(input_str) 
    fixbasexx(input_str)
    checkfreqbypandas(input_str) 
    yunying_01248_decode(input_str)  
    Manchester_decode(input_str) 
    Fence_decode(input_str) 
    # 基于词频/字典的解码
    cipin_mix_fangshe_affine(input_str.lower()) 
    try:
        my_vigenere(input_str.lower())
    except:
        pass
    vigenere_by_dictionary(input_str.lower())
    # 基于已知明文的爆破
    print("-"*20+color_string("[以下开始基于已知明文的爆破分析]",BLUE)+"-"*20)   
    # 提示请输入已知明文,RED and YELLOW
    mingwen = input("请输入"+color_string("已知明文",GREEN)+"一般是连续的前若干个字符，比如"+color_string("flag/synt",GREEN)+".\n特殊情况：输入 BURP_ALL_AFFINE ==> 强制仿射暴力输出\n直接回车可退出爆破,请输入：")
    if len(mingwen) > 0:
        flag = mingwen.lower()
        print("-"*20+color_string("[输入的已知明文是: ",YELLOW)+color_string(mingwen,RED)+"-"*20)   # modify at 20250929 
        Hill_key_burp(input_str.lower(),flag)  # modify at 20250929 
        burp_affine(input_str.lower(),flag) 
        vigenere_shortest_key_burp(input_str,mingwen)  # modify at 20250929 
        vigenere_theory_key_burp(input_str,mingwen)  # add at 20250929 

def checkfile(file):
    data=''
    with open(file,'r') as f:
        lines = f.readlines()
        for line in lines:
            txt = line.replace('\n','').strip()
            data += txt
    checktxt(data)

def showHelp():
    print('''
  参数不完整，参见以下帮助:
  -h, --help  显示帮助信息
  -f, --file  读取txt文本，不区分换行
  -t, --txt   读取输入字符串   

  例1：python3 checkascii.py -t "348ufrf4rt34rufdvzcvrt34rhfdshaskasff&)*)%&^"
       --------------------直接检测输入字符串---------------

  例2：python3 checkascii.py -f ./testfile.txt 
       --------------------读取指定文件并检测-------------------
    ''')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help='读取txt文本，不区分换行')
    parser.add_argument('-t','--txt',help='读取输入字符串')

    args = parser.parse_args()
    
    str = args.txt
    file = args.file
    if str:
        checktxt(str)
        return
    if file:
        checkfile(file)
        return
    showHelp()


if __name__ == '__main__':
    main()
