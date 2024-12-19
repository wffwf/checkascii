#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
from string_operator_module import *
# 说明:基于密钥长度的暴力破解
import string
import itertools

def vigenereCrack(cipherText, key): # 解密函数
    cipherText=cipherText.lower()
    key = key.lower()
    length = len(key)
    plainText = ''
    index = 0
    for ch in cipherText:
        if ch not in string.ascii_lowercase:
            plainText += ch
        else:
            c = chr((ord(ch)-ord(key[index%length])+26)%26+97)  #字母的ascii值与对该位置加密的密钥字母，相对位移
            plainText += c
            index+=1
    return plainText



# 基于已知的明文、密文只有4位，初步判断密钥的长度最大为4，爆破单元如下
def burpCrackUnit(input_str,m,k):
    c = input_str[0:len(m)]
    if vigenereCrack(c,k) == m:
        result = vigenereCrack(input_str,k)
        # print("vigenere Crack maybe success, the key maybe: %s, the result maybe %s" % (k,result))
        print("vigenere Crack maybe "+color_string("SUCCESS",GREEN)+", the key is: "+color_string(k,GREEN)+", the result maybe: "+color_string(result,GREEN))
    #elif otherCrack(c,k) == m:
        #print("other Crack success, the key maybe:",k)

def shortest_key_burp(c,m):
    for i in range(1,len(m)+1):
        for k in itertools.product(string.ascii_lowercase,repeat=i):
            key = ''.join(k)
            burpCrackUnit(c,m,key)

def ascii_key_burp(c,m):
    print("-"*20+color_string("[结合一段已知明文 \""+m+"\" ，爆破vigenere密钥]",PURPLE)+"-"*20)   
    if len(c) > 200:
        choose= input("输入字符较长，为避免刷屏，请确认是否继续，输入N/n退出，任意字符继续:")   
        if choose == "N" or choose == "n":
            return 
    for i in string.ascii_lowercase:
        burpCrackUnit(c,m,i)
    
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            k = i+j
            burpCrackUnit(c,m,k)
    
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            for p in string.ascii_lowercase:
                k = i+j+p
                burpCrackUnit(c,m,k)
    
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            for p in string.ascii_lowercase:
                for q in string.ascii_lowercase:
                    k = i+j+p+q
                    burpCrackUnit(c,m,k)

def vigenere_shortest_key_burp(input_str,flag):
    ascii_key_burp(input_str,flag)

if __name__ == "__main__":
    c = "pqcq{qc_m1kt4_njn_5slp0b_lkyacx_gcdy1ud4_g3nv5x0}"
    m='flag'
    ascii_key_burp(c,m)
    c = "wznqca{d4uqop0fk_q1nwofDbzg_eu}"
    m='utflag'
    # shortest_key_burp(c,m)     # 如果需要爆破的长度超过4，就需要多进程了


    c = "ihwjawjdrihzaf"
    key = "password"
    m = vigenereCrack(c,key)
    print(m)