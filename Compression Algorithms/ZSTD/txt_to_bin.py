f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\hoffmann_comp.txt",'r')
f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\final_comp.bin",'wb') # For binary format

input = lambda: f1.readline().rstrip("\r\n")

bitstring = input()
i = 0

while i<len(bitstring):
    s = bitstring[i:i+8]
    i = i+8
    while len(s)<8:
        s += '0'
    val = int(s,2)
    f2.write(bytes({val}))
