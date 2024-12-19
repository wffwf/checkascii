#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Modified： wfsec
# refer https://github.com/cyber-jack/vigenere-solver/
from collections import Counter
import string
import vigenereTools
from string_operator_module import *

def raw_input(x):
    return input(x)

def my_py3_isalpha(x):
    if x in string.ascii_lowercase:
        return True
    else:
        return False

#This function calculates the index of coincidence
def indexOfCoincidence(cipher_text):
    N            = len(cipher_text)
    freqs        = Counter(cipher_text)
    alphabet     = map(chr, range(ord('A'),ord('Z')+1)) #converts letters to numbers
    freqsum      = 0.0

    #This for loop adds letter frequencies multiplied by letter frequency minus one
    for letter in alphabet:
        freqsum += freqs[letter] * (freqs[letter]-1)

    IC = freqsum / (N*(N-1))
    return IC
    
#This functions estimates the key length using friedmans first formula
def friedmanKeyLen1(n,i):
    keyLen = ((0.027*n)/((n-1)*i-(0.038*n)+0.065))
    return keyLen

#This functions estimates the key length using friedmans second formula        
def friedmanKeyLen2(i):
    keyLen = (0.065-0.038)/(i-0.038)
    return keyLen

#This function calculates the average index of coincidence for each key
#This function returns the key with maximum average index of coincidence
def averageIC(ciphered, max_key):
    all_avgIC={} #dictionary to store all average ICs
    for key_len in range(2,max_key): #This for loop iterates through the key lengths
        iCList =[] #List of sequence ICs' for each key length
        for j in range(0,key_len):
            sequence =""
            for i in range(j, (len(ciphered)), key_len): #generates sequences for each key length
                sequence+= ciphered[i]
            iCList.append(indexOfCoincidence(sequence)) #adds the IC to IC list
        avgIC = sum(iCList)/len(iCList) #calculates the average IC using the IC List
        all_avgIC[key_len]=avgIC #Stores average IC with corresponding key into a dictionary

    maxIC = max(all_avgIC, key=all_avgIC.get) #gets key corresponding to maximum avg IC 


    #asks user if they want to print average IC table
    avgICprint = raw_input("Would you like to print average IC table?(Press Enter to continue)")
    while avgICprint not in ['Y','y','N','n','']:
        print ("Please enter Y or N")
        avgICprint = raw_input("Would you like to print average IC table?(Press Enter to continue)")
        
    if avgICprint in ['y','Y','Yes','yes']:
        print ("Period\tAvg IC")
        for k , v in all_avgIC.iteritems(): # iterating avgIC dictionary
            print ("%d\t%f" %(k,v))
    
    return maxIC #returns key with max average IC

#Helps calculate kaisiski key length  
def kaisiskiKeyLen(kaisiski):
    if kaisiski[0]*kaisiski[1]==kaisiski[2]:
        return kaisiski[2]
    else:
        return kaisiski[0]


#This function shifts the sequences of the chosen key length 26 times around the alphabet
#then it calculates the chi square value of the shifted sequences and returns the shift value
#that corresponds to the smallest chi square value 
def caesarCracker(message):
    caesarTranslated={}
    for key in range(0, 26): #All 26 shifts
        translated=''
        for symbol in message:
            num = ord(symbol)
            num -= key
            if num > ord('Z'):
                num -= 26
            elif num < ord('A'):
                num += 26
            translated += chr(num)
        chi = calculateCHI(translated)#calculates the chi square value for the shifted sequence
        caesarTranslated[key]=chi #adds the chi squeare value to chi square dictionary

        #chooses smallest chi square value from the dictionary
        minCHI = min(caesarTranslated, key=caesarTranslated.get)
        
    #for k , v in caesarTranslated.iteritems(): # iterating caesarTranslated dictionary
       # print k,"\t", v
        
    return minCHI #returns smallest chi square value for the sequence


#A function that calculates the chi square value
def calculateCHI(text):
    #print ("----------%s---------" %text)
    text=text.lower()
    #Letter frequencies in english language
    e_frq= [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
    expct_count={}
    for each in set(text):
        q=ord(each)-97
        expct_count[each]=e_frq[q]*len(text)
    chi_sqr=sum(((text.count(a)-expct_count[a])**2)/expct_count[a] for a in set(text))
    return chi_sqr

#A function that calculates the sequences of a chosen key lengths, shifts each sequence
#using the caesarCracker function, adds all the shift values into an array
#then it translates that array into letters and returns it
#the returned array is the possible polyalphabetic cipher key
def solveUsingCHI(period, ciphered):
    solution=[]
    for j in range(0,period):
            sequence =""
            for i in range(j, (len(ciphered)), period):
                sequence+= ciphered[i]
            solution.append(caesarCracker(sequence))
    for itm in range(0,len(solution)):
        solution[itm] = chr(solution[itm]+ord('A'))
    return solution

#A function borrowed from http://inventwithpython.com/vigenereCipher.py
#This function decodes a vigenere cipher knowing the key
def translateMessage(key, message, mode):
    translated = [] # stores the encrypted/decrypted message string
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keyIndex = 0
    key = key.upper()

    for symbol in message: # loop through each character in message
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # add if encrypting
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # subtract if decrypting

            num %= len(LETTERS) # handle the potential wrap-around

            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            translated.append(symbol)

    return ''.join(translated)

#Main function
def my_vigenere(cipheredORG):
    # print("---------------------- \033[1;35m[维吉尼亚词频攻击check vigenere in chars frequency by vigenereTools.py]\033[0m --------------")
    print("-"*20+color_string("[维吉尼亚词频攻击]",PURPLE)+"-"*20)        

    #Imports the cipher from the encoded.txt file
    #cipher_file  = open( 'encrypted.txt', 'rb')  
    #temp_cipheredORG  = cipher_file.read()
    #cipheredORG = ''.join(chr(x) for x in temp_cipheredORG)

    #Checks if cipher text is long enough
    #print ( "my vigenere function 2, the input string is :")
    #print (cipheredORG)
    if len(cipheredORG)<200:
        print ("Not enough cipher text \n Exiting...")
        return# quit()
    #Edits ciphered text to remove spaces and punctuation and change it to upper case
    #ciphered= ''.join(x for x in cipheredORG if x.isalpha())
    ciphered = ''
    for x in cipheredORG:
        #print (hex(x))
        if my_py3_isalpha(x):
            #print (chr(x))
            ciphered += x
    #print (ciphered)
    ciphered=ciphered.upper()

    #Calculates friedmans index of coincidence
    friedman = indexOfCoincidence(ciphered)

    #English language IC and random text IC
    randomLetterProbability=[0.065, 0.038]


    print ("Index of Coincidence is %f" %friedman)

    #A value of IC near 0.065 would indicate that a monoalphabetic cipher was used
    #A value of IC near 0.038 would indicate that a polyalphabetic cipher was used
    #This if statement compares the result IC to the twovalues
    if (min(randomLetterProbability, key=lambda x:abs(x-friedman))== 0.065):
        print ("This suggests that a monoalphabetic cipher was used")
        print ("Using a dictionary attack...")
        #subsolve.main()
        #subsolve.main(cipheredORG)
        #raw_input("Press Enter to exit...")
    elif(min(randomLetterProbability, key=lambda x:abs(x-friedman)) == 0.038):
        print ("This suggests that a polyalphabetic cipher was used.")
            #Asks user for maximum key length
        max_key= raw_input("Please enter the maximum key length (default = 15) -->")
        if type(max_key) != int: #if user did not enter a value or entered some text
            max_key = 15
        
        print ("Estimating key length...")
        
        #Calculates friedmans estimates of key length using the functions above
        print ("Freidmans key estimation 1: %f" %friedmanKeyLen1((len(ciphered)+0.0), friedman))
        print ("Freidmans key estimation 2: %f" %friedmanKeyLen2(friedman))
        #Estimates the key based on the kaisiski analysis
        kaisiski = vigenereTools.kasiskiExamination(ciphered)
        kaisiskiPrint = raw_input("Would you like to print the kaisiski key space?(Press Enter to continue)")
        #print (kaisiskiPrint)
        while kaisiskiPrint not in ['Y','y','N','n','']:
            print ("Please enter Y or N")
            kaisiskiPrint = raw_input("Would you like to print the kaisiski key space?(Press Enter to continue)")
        
        if kaisiskiPrint in ['y','Y','Yes','yes']:
            print ("The kaisiski analysis suggests the following keyspace %d" % kaisiski)
            
        print ("The kaisiski analysis suggests that we have a period of %d" % kaisiskiKeyLen(kaisiski))

        #Estimates the key length based on the average IC
        maxIC = averageIC(ciphered, max_key)
        print ("The average IC analysis suggests that we have a period of %d" % maxIC)

        #Asks the user to enter a key length that they see fit based on the three previous tests
        while True:
            try:
                userKeyLen = int(input("Which key length would you like to use for the CHI Square analysis?"))
            except ValueError:
                print('Invalid input. Try again.')
            except SyntaxError:
                print('Invalid input. Try again.')
            except NameError:
                print('Invalid input. Try again.')
            else:
                break

        #print (hex(userKeyLen))
        #Passes the entered key length value to the solveUsingCHI function that returns the possible key
        key = solveUsingCHI(userKeyLen, ciphered)
        keyword= ''.join(key)
        print ("Your key might be %s" % keyword)
        #Tries to decode the message using the found key
        raw_input("Press Enter to decode the message using the above key...")
        translated = translateMessage(keyword, cipheredORG, 'decrypt')
        print (translated)
        #raw_input("Press Enter to exit...")


#What does this do?
#Answer here --> https://stackoverflow.com/questions/419163/what-does-if-name-main-do
#if __name__ == '__main__':
#    main()

def decode_vigenere_1 (string):

    lenString = float(len(string))

    # Find coincidence vector while looping in j == j+1. If it is equal we add
    # one in the coincidence vector. The position with the biggest coincidence
    # value is the size of the key.
    coincidences = [0]
    for i in range(1, len(string)):
            coincidences.append(0)
            for j in range(0, len(string)):
                if(string[j] == string[(j+i)%len(string)]):
                    coincidences[i] += 1

    keylength = coincidences.index(max(coincidences))
    print('Key Length: %d' % keylength)

    # Letter frequency in english language
    letterFrequency = [
        8.167, 1.492, 2.782, 4.253, 12.702, 2.015, 6.094, 2.228, 6.966, 0.153,
        0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
        2.758, 0.978, 2.360, 0.150, 1.974, 0.074
    ]

    key = ''
    # We need to find a character for each poisition in the key
    for i in range(0, keylength):
        # Here we are reseting the values
        textFrequency = {}
        maxValue = -1
        maxPosition = 0
        rolledArray = letterFrequency

        # For each character in the alphabet we need to find the biggest sum value
        # while alling it to some letter.
        for j in range(0, 26):
            if(j > 0):
                rolledArray = np.roll(rolledArray, 1)

            for k in range(0, 26):
                textFrequency[chr(k + 97)] = 0

            # Find the frequency of the positions in the key. We loop through the
            # string using the keylength and start at the position we want to find
            # the character for
            k = i;
            while(k < lenString):
                letter = string[k]
                textFrequency[letter] += 1/lenString * 100
                k += keylength;

            # Sum the values of textFrequency * rolledArray
            sumValues = 0;
            for k in range(0, 26):
                sumValues += textFrequency[chr(k + 97)] * rolledArray[k];

            # The biggest value wins
            if(sumValues > maxValue):
                maxValue = sumValues
                maxPosition = j

        # Since we loop for all the alphabet we know who is the owner of the biggest sum,
        # so we found one character of our key
        key += chr(maxPosition + 97)

    keyAsInt = [ord(i) for i in key]
    cipherAsInt = [ord(i) for i in string]
    plainText = ''

    # We have the key now we just need to decipher it! :)
    for i in range(0, int(lenString)):
        value = (cipherAsInt[i] - keyAsInt[i % keylength]) % 26
        plainText += chr(value + 97)

    print('Key: %s\n' % key)
    print('Decipher key: %s' % plainText)




if __name__ == '__main__':
    c=open('vige.txt','r').read()
    my_vigenere(c)
