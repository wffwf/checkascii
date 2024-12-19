#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
from string_operator_module import *
import gmpy2
import sys
import string
BURP_ALL_AFFINE = 'BURP_ALL_AFFINE'
def affine_decrypt(ciphertext, a, b):
    plaintext = ""
    inverse_a = 0
    for i in range(26):
        if (a * i) % 26 == 1:
            inverse_a = i
            break
 
    for char in ciphertext:
        if char.isalpha():
            char_num = ord(char) - ord('A')
            decrypted_char_num = (inverse_a * (char_num - b)) % 26
            decrypted_char = chr(decrypted_char_num + ord('A'))
            plaintext += decrypted_char
        else:
            plaintext += char
 
    return plaintext
 
def affine_decrypt_A(info, a, b): # 符合标准的仿射解密
    try:
        reverse_a = gmpy2.invert(a, 26) #求a的逆元
        res = ""
        for x in info:
            if x <= "z" and x >= "a":
                res += chr((reverse_a*((string.ascii_lowercase.index(x))-b))%26+ord("a")) #d(x)=a的逆元(x-b)(mod 26)
            elif x <= "Z" and x >= "A":
                res += chr((reverse_a*((string.ascii_uppercase.index(x))-b))%26+ord("A"))
            else:
                res += x
        return res.upper()
    except:
        return ""

def brute_force(ciphertext,flag):
    FLAG = flag.upper()
    for a in range(1, 26,2): # a,必须是（1,3,5,7,9,11,15,17,19,21,23,25）中的一个
        for b in range(26):# b,0~25
            plaintext = affine_decrypt_A(ciphertext, a, b)
            if FLAG == BURP_ALL_AFFINE:
                print(f"Using key: a={a}, b={b} -> ",end='')
                print(color_string(plaintext,GREEN))
            elif FLAG in plaintext:
                print(f"Using key: a={a}, b={b} -> ",end='')
                print(color_string(plaintext,GREEN))

def burp_affine(c,flag):
    print("-"*20+color_string("[仿射密码affine爆破:c = [i*p + j]%26. i,j,均未知需要爆破]",PURPLE)+"-"*20)   

    if len(c) > 200:
        choose= input("输入字符较长，为避免刷屏，请确认是否继续，输入N/n退出，任意字符继续:")   
        if choose == "N" or choose == "n":
            return 

    brute_force(c.lower(),flag)



if __name__ == "__main__":
    c=open('vigenere_shortest.txt','r').read()
    burp_affine(c,'flag')
    atbash = "UOZTSZSZXGURHMRXV"
    burp_affine(atbash,'flag')    
    caesar = " mshn{jhlzhy_pz_mbuufek}"
    burp_affine(caesar,'flag')    
    c = "zrckewsgnpaovhat"
    burp_affine(c,BURP_ALL_AFFINE)   
    c = "prwy{w14wf3p5-fo6w-11gf-w02o-88g9pg5197wo}"
    burp_affine(c,'flag')
