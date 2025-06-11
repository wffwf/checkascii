#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
import base64 as b64
import base36 as b36
import base58 as b58
import base91 as b91
import py3base92 as b92
import base62 as b62
from string_operator_module import *
from z85 import *
import base45 as b45

def sort_asc(input_str):
    listl = list(input_str)
    lists = list(set(listl))
    lists.sort(key=listl.index)
    lists.sort()
    res=""
    for i in lists:
        res = res + i
    return res

def matchstring(input_str,dest):
    for i in input_str:
        if dest.find(i) == -1:
            return -1
    return 0
# TODO

# END TODO

def tryBase16(input_str):
    base16="0123456789ABCDEF"
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base16) == 0:
        try:
            b16 = b64.b16decode(input_str.encode('utf-8')).decode()
            print("maybe "+color_string("SUCCESS",GREEN)+" [base16] string "+", decode result is "+color_string(b16,GREEN))
        except:
            pass
def tryBase32(input_str):
    base32="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567="
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base32) == 0:
        try:
            b32 = b64.b32decode(input_str.encode('utf-8')).decode()
            print("maybe "+color_string("SUCCESS",GREEN)+" [base32] string "+", decode result is "+color_string(b32,GREEN))            
        except:
            b32 = errinfo
def tryBase36(input_str):
    base36="0123456789abcdefghijklmnopqrstuvwxyz"
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base36) == 0:
        try:
            reb36 = b36.dumps(int(input_str))
            print("maybe "+color_string("SUCCESS",GREEN)+" [base36] string "+", decode result is "+color_string(reb36,GREEN))                        
        except:
            reb36 = errinfo
def tryBase45(input_str):
    try:
        reb45 = b45.b45decode(input_str.encode('utf-8')).decode()
        print("maybe "+color_string("SUCCESS",GREEN)+" [base45] string "+", decode result is "+color_string(reb45,GREEN))                        
    except:
        pass
def tryBase58(input_str):
    base58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base58) == 0:
        try:
            reb58 = b58.b58decode(input_str.encode('utf-8')).decode()
            # print("maybe SUCCESS [base58] string  %s, decode result is %s"%(sort_asc(base58),reb58))
            print("maybe "+color_string("SUCCESS",GREEN)+" [base58] string "+", decode result is "+color_string(reb58,GREEN))
        except:
            reb58 = errinfo
def tryBase62(input_str):
    base62="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base62) == 0:
        try:
            reb62 = b62.decodebytes(input_str)
            # print("maybe SUCCESS [base62] string  %s, decode result is %s"%(sort_asc(base62),reb62))
            print("maybe "+color_string("SUCCESS",GREEN)+" [base62] string "+", decode result is "+color_string(reb62,GREEN))                        
        except:
            reb62 = errinfo
def tryBase64(input_str):
    base64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base64) == 0:
        try:
            input_strmod4 = len(input_str) % 4
            if input_strmod4 == 2:
                input_str = input_str + "=="
            if input_strmod4 == 3:
                input_str = input_str + "=" 
            reb64 = b64.b64decode(input_str.encode('utf-8')).decode()
            print("maybe "+color_string("SUCCESS",GREEN)+" [base64] string "+", decode result is "+color_string(reb64,GREEN))                        
        except:
            reb64 = errinfo

def tryBase85(input_str):
    if input_str.startswith("<~"):
        input_str = input_str[2:]
    if input_str.endswith("~>"):
        input_str = input_str[:-2]
    # Standard Base 85
    try:
        reb85 = b64.a85decode(input_str.encode('utf-8')).decode()
        print("maybe "+color_string("SUCCESS",GREEN)+" [base85-standard] string "+", decode result is "+color_string(reb85,GREEN))                        
    except:
        pass
    # RFC 1924 (IPV6)
    try:
        reb85 = b64.b85decode(input_str.encode('utf-8')).decode()
        print("maybe "+color_string("SUCCESS",GREEN)+" [base85-rfc-1924-IPV6] string "+", decode result is "+color_string(reb85,GREEN))                        
    except:
        pass
    # ZeroMQ Z85
    try:
        reb85 = z85decode(input_str.encode('utf-8'))
        print("maybe "+color_string("SUCCESS",GREEN)+" [base85-ZeroMQ-Z85] string "+", decode result is ",end='')
        print(reb85)                        
    except:
        pass

def tryBase91(input_str):
    base91="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\""
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base91) == 0:
        try:
            reb91 = b91.decode(input_str).decode()
            print("maybe "+color_string("SUCCESS",GREEN)+" [base91] string "+", decode result is "+color_string(reb91,GREEN))                        
        except:
            reb91 = errinfo            
def tryBase92(input_str):
    base92="!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}"
    errinfo = 'DECODE FAILED!'
    if matchstring(input_str,base92) == 0:
        try:
            reb92 = b92.b92decode(input_str).decode()
            print("maybe "+color_string("SUCCESS",GREEN)+" [base92] string "+", decode result is "+color_string(reb92,GREEN))                        
        except:
            reb92 = errinfo
def tryBase100(input_str):
    pass # emoji to text I gived up

def checkbasexx(input_str):
    input_strLen = len(input_str)
    print("-"*20+color_string("[Base不全家桶check]",PURPLE)+"-"*20)
    print("the input_str string  [length] is %d"%input_strLen)
    if input_strLen > 1000:
            print(color_string("字符较长，base解码可能有延迟，按CTRL+C可取消",PURPLE))
    print("the characters in [input_strs] string is %s"%sort_asc(input_str))
    tryBase16(input_str)
    tryBase32(input_str)
    tryBase36(input_str)
    tryBase45(input_str)
    tryBase58(input_str)
    tryBase62(input_str)
    tryBase64(input_str)
    tryBase85(input_str)
    tryBase91(input_str)
    tryBase92(input_str)

def fixbasexx(input_str):
    input_strLen = len(input_str)
    if input_strLen > 1000:
            print("-"*20+color_string("字符较长，fix base不支持",PURPLE)+"-"*20)
    else:    
        print("-"*20+color_string("[Base不全家桶fix&check]",PURPLE)+"-"*20)   
        FIXBYTES = input_strLen - 8
        FIXINFOSTRING = "[本次fix输入的前后"+str(FIXBYTES)+"个字符]"
        print("-"*20+color_string(FIXINFOSTRING,PURPLE)+"-"*20)       
        FIXTAILS = 8
        FIXTAILSTRING = "[本次fix输入后"+str(FIXBYTES)+"个等于(=)符号]"
        print("-"*20+color_string(FIXTAILSTRING,PURPLE)+"-"*20)       
        print("the input_str string  [length] is %d"%input_strLen)
        print("the characters in [input_strs] string is %s"%sort_asc(input_str))    
        for i in range(1,1+FIXBYTES):
            tryBase16(input_str[:(-i)])
            tryBase16(input_str[i:])
            tryBase32(input_str[:(-i)])
            tryBase32(input_str[i:])
            tryBase36(input_str[i:])
            tryBase36(input_str[:(-i)])
            tryBase45(input_str[:(-i)])
            tryBase45(input_str[i:])
            tryBase58(input_str[:(-i)])
            tryBase58(input_str[i:])
            tryBase62(input_str[:(-i)])
            tryBase62(input_str[i:])
            tryBase64(input_str[:(-i)])
            tryBase64(input_str[i:])
            tryBase85(input_str[:(-i)])
            tryBase85(input_str[i:])
            tryBase91(input_str[:(-i)])
            tryBase91(input_str[i:])
            tryBase92(input_str[i:])        
            tryBase92(input_str[:(-i)])   
        for i in range(1,1+FIXTAILS):
            tryBase16(input_str+"="*i)
            tryBase32(input_str+"="*i)
            tryBase36(input_str+"="*i)
            tryBase45(input_str+"="*i)
            tryBase58(input_str+"="*i)
            tryBase62(input_str+"="*i)
            tryBase64(input_str+"="*i)
            tryBase85(input_str+"="*i)
            tryBase91(input_str+"="*i)
            tryBase92(input_str+"="*i)    
def main():
    a16 = "756E6374667B64383537303366396630363734343162313632613363663337363635346662627D"
    checkbasexx(a16)
    a32="OVXGG5DGPNSDQNJXGAZWMOLGGA3DONBUGFRDCNRSMEZWGZRTG43DMNJUMZRGE7I="
    checkbasexx(a32)
    a36 = "3260642638018773869442264770789901583439875515599863956359"
    checkbasexx(a36)
    a45 = "2%EZPC0/C6UCXW6946O-CF-CJ%6:Q6.A6/96RG6FM6I-C4:6H%64S6VJCZ2"
    checkbasexx(a45)
    a58 = "2Kg5PqrKEivTvM5ntvFAzq7uKcVWWUGHTh3cbqfErZL2zD8i58szur"
    checkbasexx(a58)
    a62 = "2OE2u1B6wRK8Rzc0gB3D7J4xWjKCrQTAVXAKTjExR7cCZ6z0PsuZ3"
    checkbasexx(a62)
    a64 = "dW5jdGZ7ZDg1NzAzZjlmMDY3NDQxYjE2MmEzY2YzNzY2NTRmYmJ9"
    checkbasexx(a64)
    a91 = "9o(IF.TZ_27=?j`juRYx;m7X7Iq*@YQiAJv<:m{igJ(1;aIs"
    checkbasexx(a91)
    a92 = "K<jslc7b9fGHjgXV62h[o9X39Wh'=:Uc4(H8k%XSDwFpW^)!"
    checkbasexx(a92)
    a85 = open('base85.txt','r').read()
    checkbasexx(a85)
    a85_b = open('base85-b.txt','r').read()
    checkbasexx(a85_b)
    a85_c = open('base85-z.txt','r').read()
    checkbasexx(a85_c)   
    fix = "MZWGCZ33MZUW4ZC7OJSWC3C7O5QXSX3UNBQW4X3ZN52V6Y3BNZPXO2LOPU======="
    fixbasexx(fix)

if __name__ == "__main__":
    main()
