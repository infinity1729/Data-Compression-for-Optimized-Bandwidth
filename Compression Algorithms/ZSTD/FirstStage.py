class LZW:

    def compress(uncompressed : str):
        """Compress a string to a list of output symbols."""

        # Build the dictionary.
        dict_size = 256
        dictionary = {chr(i):i for i in range(dict_size)}

        f3 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\top_1000_words.txt",'r')
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
        # print(result)

        return result

    def decompress(compressed : list): 
        """Decompress a list of output ks to a string."""
        
        # ReBuild the dictionary.
        dict_size = 256
        dictionary = dict((i, chr(i)) for i in range(dict_size))

        f3 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\top_1000_words.txt",'r')
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
                raise ValueError(f'Bad compressed {k}')
            result.append(entry)

            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry

        # print(result.getvalue())
        return ''.join(result)

################################################ DRIVER CODE ####################################################

lzw = LZW

f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\bible.txt",'r')
f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\lzw_comp.txt",'w') # For text format

input = lambda: f1.readline().rstrip("\r\n")

# f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\bible_comp.bin",'wb') # For binary format

total_lines = 30382
total_content = []

for _ in range(total_lines):
    s = input()
    total_content.append(s)
    total_content.append('\n')
    
s = ''.join(total_content)
total_orig_chr = len(s)*8

l = lzw.compress(s)
f2.write(str(len(l))+'\n')

# last = 0
for i in l:
    f2.write(str(i)+' ')
    # last = i

# mx = 0

# for i in l:
#     mx = max(mx,i) # Find the max Ascii value obtained 

# base = ceil(log(mx,2)) # Number of bits needed to represent this.
# bitstring = []

# for i in l:
#     x = bin(i)[2:]
#     x = (base-len(x))*'0'+x
#     bitstring.append(x)

# i = 0
# bitstring = ''.join(bitstring)

# while i<len(bitstring):
#     s = bitstring[i:i+8]
#     i = i+8
#     while len(s)<8:
#         s += '0'
#     val = int(s,2)
#     f2.write(bytes({val}))

# total_compressed_chr = len(l)*base

# c_ratio = total_compressed_chr/total_orig_chr

# print(c_ratio)

# ###################### LZW - Decompress

# f1 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\lzw_comp.txt",'r')
# f2 = open("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\bible_decomp.txt",'w')

# n = input()
# l = list(map(int,input().split()))
# decomp = lzw.decompress(l)
# print(decomp)
# f2.write(decomp)