from collections import OrderedDict
import time

def decompress(compressed : list): 
    """Decompress a list of output ks to a string."""
    
    # ReBuild the dictionary.
    dict_size = 256
    dictionary = OrderedDict({i:chr(i) for i in range(dict_size)})

    f3 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\DictionaryBased\\top_1000_words.txt",'r')
    input2 = lambda: f3.readline().rstrip("\r\n")

    for i in range(999): # Number of words in f3
        s = input2()
        dictionary[dict_size] = s
        dict_size += 1

    # The logic here is to decompress and build the dictionary side by side.

    w = chr(compressed.pop(0))
    result = [w]

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            # return ''.join(result)
            raise ValueError(f'Bad compressed {k}')
        result.append(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    # print(result.getvalue())
    return ''.join(result)

################################################ DRIVER CODE ####################################################

# f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\LZW\\lzwComp.txt",'r')
f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\DictionaryBased\\Decomp.txt",'w',encoding='utf-8') # For text format
f4 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\DictionaryBased\\Comp.bin",'rb') # For text format

# input = lambda: f1.readline().rstrip("\r\n")

# l = list(map(int,input().split()))
# decomp = decompress(l)
# f2.write(decomp)

s = f4.read()
msg = s.decode(encoding = "ISO-8859-1")

base = ord(msg[0])
# print(base)

bitstring = []
for i in range(1,len(msg)):
    s = bin(ord(msg[i]))[2:]
    bitstring.append((8-len(s))*'0'+s)

bitstring = ''.join(bitstring)
l = []
i = 0
while i<len(bitstring):
    s = bitstring[i:i+base]
    l.append(int(s,2))
    i += base

start = time.time()
decomp = decompress(l)
end = time.time()

print("Decompression done in ",end-start," seconds")
f2.write(decomp)