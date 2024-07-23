from collections import OrderedDict
from decimal import *
import time

block_size = 250
getcontext().prec = 340

class ArithmeticEncoding:

    def encode(message):

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for term in message:
            diff = Decimal(stage_max-stage_min)
            stage_min = stage_min+cond_prob_table[term]*diff
            stage_max = stage_min+prob_table[term]*diff
        return (stage_min+stage_max)/2
    
    def decode(message):
        
        msg = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for _ in range(block_size):

            diff = stage_max - stage_min

            left = 0
            right = len(keys)-2

            while left<=right:
                mid = (left+right)//2

                if message >= (stage_min + cond_prob_table[keys[mid]]*diff):
                    left = mid+1
                else:
                    right = mid-1

            msg.append(keys[right])
            x = stage_min

            stage_min = x + cond_prob_table[keys[right]]*diff
            stage_max = x + cond_prob_table[keys[right+1]]*diff

        return ''.join(msg)

ae = ArithmeticEncoding

f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\AE\\Sensible Data\\bible.txt",'r')
f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\AE\\Sensible Data\\bibleComp.txt",'w') # For text format
f3 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\AE\\Sensible Data\\bibleComp.bin",'wb') # For text format

input = lambda: f1.readline().rstrip("\r\n")

# f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\bible_comp.bin",'wb') # For binary format

freq = OrderedDict({'I': 12823, 'n': 215496, ' ': 766111, 't': 299633, 'h': 270179, 'e': 396042, 'b': 42888, 'g': 47279, 'i': 174140, 'G': 5943, 'o': 226152, 'd': 144021, 'c': 51317, 'r': 157355, 'a': 248716, 'v': 29448, '.': 25438, 'A': 17038, 'w': 61051, 's': 179075, 'u': 80762, 'f': 78370, 'm': 74364, ',': 68389, ';': 9968, 'k': 20703, 'p': 39885, 'S': 4618, '\n': 30382, 'L': 8859, 'l': 117300, ':': 12439, 'D': 8425, 'y': 56323, 'N': 1746, 'H': 3042, 'E': 2439, 'B': 4472, 'x': 1423, 'T': 7424, 'O': 8547, 'R': 7179, 'P': 1718, 'W': 2345, 'M': 2954, 'Y': 529, '?': 3179, 'F': 2292, 'U': 275, "'": 1943, 'C': 1621, 'j': 2388, 'Z': 883, 'J': 5920, 'q': 930, 'z': 1828, 'K': 519, '(': 214, ')': 214, '!': 308, 'V': 99, '-': 23, 'Q': 5})

s = Decimal(sum(list(freq.values())))
prob_table = OrderedDict({i:Decimal(freq[i])/s for i in freq})
cond_prob_table = OrderedDict()
s = Decimal(0.0)

for i in prob_table:
    cond_prob_table[i] = s
    s += prob_table[i]

# print(prob_table)

total_lines = 30382
total_content = []

for _ in range(total_lines):
    s = input()
    total_content.append(s+'\n')

s = ''.join(total_content)
s += (block_size-len(s)%block_size)%block_size * ' '

total_lines = len(s)//block_size

bitstring = []

start = time.time()
for i in range(total_lines):
    st = s[block_size*i : block_size*i+block_size]
    msg = ae.encode(st)
    x = str(msg)[2:][::-1]
    st = bin(int(x))[2:]
    bitstring.append(st)
    f2.write(str(msg)+'\n')

bitstring = ''.join(bitstring)

while i+8<len(bitstring):
    s = bitstring[i:i+8]
    i = i+8
    val = int(s,2)
    f3.write(bytes({val}))

end = time.time()

print("Compression Done!")
print(f"Compression time: {end-start} seconds")

####################### DE Compress #######################

f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\AE\\Sensible Data\\bibleComp.txt",'r') # For text format
f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\AE\\Sensible Data\\bibleDecomp.txt",'w') # For text format

start = time.time()

cond_prob_table['dc'] = Decimal(1.0)
keys = list(cond_prob_table.keys())

for _ in range(total_lines):
    s = Decimal(input())
    msg = ae.decode(s)
    
    f2.write(str(msg))

end = time.time()

print("Decompression Done!")
print(f"Decompression time: {end-start} seconds")