from collections import OrderedDict
from math import log,ceil
import time

def compress(uncompressed : str):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = OrderedDict({chr(i):i for i in range(dict_size)})

    f3 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\DictionaryBased\\top_1000_words.txt",'r')
    input2 = lambda: f3.readline().rstrip("\r\n")

    for i in range(999): # Number of words in f3
        s = input2()
        dictionary[s] = dict_size
        dict_size += 1

    # The logic is to keep considering the new characters till they are already present in the dictionary. Say you already have the string s[:i] in the dictrionary. You are now considering the string s[:i+1]. Now if this is also present in the dictionary already keep going untill u find a character which makes the string till i not present. Now you consider your next word starting from this character.

    # The intuition behind why this works is that you keep on clubbing the maximum possible word together and hence it will reduce the final entropy of the string found, although it might not result in the minimum possible entropy   ( compression ).

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary: 
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])

    return result

################################################ DRIVER CODE ####################################################

f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\bible.txt",'r')
# f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\DictionaryBased\\Comp.txt",'w') # For text format

f4 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\DictionaryBased\\Comp.bin",'wb') # For text format

input = lambda: f1.readline().rstrip("\r\n")

# f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\bible_comp.bin",'wb') # For binary format

total_lines = 30382
total_content = []

for _ in range(total_lines):
    s = input()
    total_content.append(s+'\n')
    
s = ''.join(total_content)
total_orig_chr = len(s)*8

l = compress(s)

# for i in l:
#     f2.write(str(i)+' ')

mx = 0

for i in l:
    mx = max(mx,i) # Find the max Ascii value obtained 

base = ceil(log(mx,2)) # Number of bits needed to represent this.
bitstring = []

for i in l:
    x = bin(i)[2:]
    x = (base-len(x))*'0'+x
    bitstring.append(x)

i = 0
bitstring = ''.join(bitstring)

start = time.time()

f4.write(bytes({base}))
# print(base)

while i+8<len(bitstring):
    s = bitstring[i:i+8]
    i = i+8
    val = int(s,2)
    f4.write(bytes({val}))

end = time.time()

print("Compression done in ",end-start," seconds")
