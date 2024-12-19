#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Modified： wfsec
from string_operator_module import *
# refer https://github.com/cyber-jack/vigenere-solver/
# Substitution cipher solver by Joseph Connor <josephc346@gmail.com>


def is_match(word, cword, mapping):
    """Check if a word could be a match under current mapping"""

    if len(word) != len(cword): 
        return False

    # make a copy mapping to work with
    mapping = {c : a.copy() for c, a in mapping.items()}

    for pc, cc in zip(word, cword):
        # if the ciphertext char could map to the plain char, assume it does
        if pc in mapping[cc]:
            for c in mapping.keys():
                mapping[c] -= set([pc])
            mapping[cc] = set([pc])
        else:
            # Otherwise it can't be a match
            return False
    return True


def get_matches(cword, mapping, dictionary):
    """Return a list of matching words under the current mapping"""
    return [word for word in dictionary if is_match(word, cword, mapping)]


def prune(mapping):
    """Remove reduntant entries from the mapping"""
    can_prune = True
    while can_prune:
        can_prune = False
        for c in mapping.keys():
            # If any character has only one possible mapping,
            # remove that character as a possible mapping for others
            if len(mapping[c]) == 1:
                pc = list(mapping[c])[0]
                for k in mapping.keys():
                    if k != c and pc in mapping[k]:
                        can_prune = True
                        mapping[k] -= set([pc])
            
            
def solve(ciphertext, alphabet, dictionary):
    """Attempt to solve the substitution cipher"""
    punctuation = " '-"

    # Maps ciphertext characters to their possible plaintext counterparts
    mapping = {c : set(alphabet) for c in alphabet}
    mapping.update({p : set([p]) for p in punctuation})
    
    # We don't really care about whitespace, just make it all the same
    ciphertext = ciphertext.lower().replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')

    # Filter out all characters not in the alphabet or relevant puncuation
    ciphertext = ''.join(c for c in ciphertext if c in alphabet or c in punctuation)
    cipher_words = ciphertext.split(' ')

    did_something = True
    while did_something:
        did_something = False
        start_len = sum(len(s) for s in mapping.values())

        for cword in cipher_words:
            if cword == '':
                continue

            matches = get_matches(cword, mapping, dictionary)

            if len(matches) == 0:
                print(color_string("No possible solutions found for "+cword+" kick it and try again",YELLOW))
                print(color_string("The plaintext probably contains some word that isn't in our dictionary.",BLUE))
                return mapping,cword

            # Remove all possible mappings for each character in this word
            for cc in cword:
                mapping[cc] = set()

            # Now add back possible mappings based on matches
            for match in matches:
                for pc, cc in zip(match, cword):
                    mapping[cc] |= set([pc])

            # Remove some impossible mappings
            prune(mapping)

        end_len = sum(len(s) for s in mapping.values())
        if end_len < start_len:
            did_something = True

    return mapping


def usage():
    print("usage: python subsolve.py wordlist-file ciphertext-file")
    sys.exit(1)


def vigenere_by_dictionary(c):
    print("-"*20+color_string("[维吉尼亚字典攻击]",PURPLE)+"-"*20)        

    word_list = 'wordlist.dic'
    ciphertext = c.lower()
    # read word list and ciphertext from files
    with open(word_list, 'r') as f:
        dictionary = [w.strip() for w in f.read().replace('\r', '').split('\n')]
        dictionary = [w for w in dictionary if not w.startswith('#') and not w == '']
    # solve
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(10):
        try:
            mapping,cword = solve(ciphertext, alphabet, dictionary)
        except:
            return
        # replace known letters with their plaintext counterparts
        solution = ciphertext
        for cc, pcs in mapping.items():
            if len(pcs) == 1:
                solution = solution.replace(cc, list(pcs)[0].upper())
        print(solution)
        # kick the unknow strings and slove for 10 times
        ciphertext=ciphertext.replace(cword,'')

def example():
    #if len(sys.argv) != 3:
        #usage()

    word_list = 'wordlist.dic'
    cipher_file = 'vige2.txt'

    # read word list and ciphertext from files
    with open(word_list, 'r') as f:
        dictionary = [w.strip() for w in f.read().replace('\r', '').split('\n')]
        dictionary = [w for w in dictionary if not w.startswith('#') and not w == '']
    with open(cipher_file, 'r') as f:
        ciphertext = f.read().lower()

    # solve
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(10):
        mapping,cword = solve(ciphertext, alphabet, dictionary)

        # print possible mappings
        #for cc in mapping.keys():
            #print("%s = %s" % (cc, ', '.join(mapping[cc])))

        # replace known letters with their plaintext counterparts
        solution = ciphertext
        for cc, pcs in mapping.items():
            if len(pcs) == 1:
                solution = solution.replace(cc, list(pcs)[0].upper())
        print(solution)
        # print(cword)
        ciphertext=ciphertext.replace(cword,'')

if __name__ == '__main__':
    c=open('vige2.txt','r').read()
    vigenere_by_dictionary(c)
