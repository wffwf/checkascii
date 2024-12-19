#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
import string
RED = 31 # FAILED COLOR
GREEN = 32 # SUCCESS COLOR
YELLOW = 33 # WARN COLOR
BLUE = 34 # STEP COLOR
PURPLE = 35 # SECTION COLOR
def color_string(a,color):
    if type(a) == type("string"):
        return("\033[1;"+str(color)+"m"+a+"\033[0m")
    if type(a) == type(b"string"):
        try:
            u = a.decode('utf-8')
            return("\033[1;"+str(color)+"m"+u+"\033[0m")
        except:
            return(a)