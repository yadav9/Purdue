#!/usr/bin/env python3


import sys
sys.path.append("/home/kanishk/Desktop/ECE404/HW2")
from BitVector import *


################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8,
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19,
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

row_perm = [0, 5]
col_perm = [1, 2, 3, 4]


###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
with open('s-box-tables.txt') as f:
    arrays = []

    for line in f:
        x = line.split()
        if(len(x) == 16):
            x = [int(i) for i in x]
            arrays.append(x)

    s_box = []

    for i in range(0,32, 4):
        s_box.append([arrays[k] for k in range(i, i+4)]) # S_BOX

#    print(s_box)

#######################  Get encryptin key from user  ###########################

def get_encryption_key(): # key
    ## ask user for input

    ## make sure it satisfies any constraints on the key

    file_key = input("Enter key file with 8 character key: ")

    with open(file_key) as file:
        file_length = len(file.read())

    ## next, construct a BitVector from the key
    b_v = BitVector(filename = file_key)
    user_key_bv = b_v.read_bits_from_file(64)
    key_bv = user_key_bv.permute( key_permutation_1 )        ## permute() is a BitVector function
    return key_bv


################################# Generatubg round keys  ########################
def extract_round_key( nkey ): # round key
    round_key = []

    for i in range(16):
         [left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
         shift = shifts_key_halvs[i]
         left << shift
         right << shift
         nkey = left + right
         perm = nkey.permute(key_permutation_2)
         round_key.append(perm)
    return round_key


########################## encryption and decryption #############################

def des(fin, fout_1, fout_2, key):

    encrypted_text = encrypt(fin, fout_1, key)
    decrypt(encrypted_text, fout_2, key)
        ## write code to carry out 16 rounds of processing


def encrypt(fin,fout_1,key):
    FILEOUT = open(fout_1,'w')
    with open (fin) as f:
        file_len = len(f.read())

    file_write = (8 - (file_len % 8)) % 8



    with open(fin, 'a') as f:
        f.write(' ' * file_write)

    bv = BitVector(filename = fin)
    final = BitVector(size = 0)


    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(64)

        [L,R] = bitvec.divide_into_two()    #split into 2
        round_key = extract_round_key(key)    #extract key

        for i in range (16):
            saved_R = R
            expanded = R.permute(expansion_permutation)
            expanded = expanded ^ round_key[i]

            [one, five] = expanded.divide_into_two()
            [one, three] = one.divide_into_two()
            [one, two] = one.divide_into_two()
            [three, four] = three.divide_into_two()
            [five, seven] = five.divide_into_two()
            [five, six] = five.divide_into_two()
            [seven, eight] = seven.divide_into_two()

            # S-box substitution
            row=one.permute(row_perm).int_val()
            col=one.permute(col_perm).int_val()
            one = BitVector(intVal=s_box[0][row][col], size=4)

            # S-box substitution
            row=two.permute(row_perm).int_val()
            col=two.permute(col_perm).int_val()
            two = BitVector(intVal=s_box[1][row][col], size=4)

            # S-box substitution
            row=three.permute(row_perm).int_val()
            col=three.permute(col_perm).int_val()
            three = BitVector(intVal=s_box[2][row][col], size=4)

            # S-box substitution
            row=four.permute(row_perm).int_val()
            col=four.permute(col_perm).int_val()
            four = BitVector(intVal=s_box[3][row][col], size=4)

            # S-box substitution
            row=five.permute(row_perm).int_val()
            col=five.permute(col_perm).int_val()
            five = BitVector(intVal=s_box[4][row][col], size=4)

            # S-box substitution
            row=six.permute(row_perm).int_val()
            col=six.permute(col_perm).int_val()
            six = BitVector(intVal=s_box[5][row][col], size=4)

            # S-box substitution
            row=seven.permute(row_perm).int_val()
            col=seven.permute(col_perm).int_val()
            seven = BitVector(intVal=s_box[6][row][col], size=4)

            # S-box substitution
            row=eight.permute(row_perm).int_val()
            col=eight.permute(col_perm).int_val()
            eight = BitVector(intVal=s_box[7][row][col], size=4)

            # Combine the eight keys
            before_p_box = one + two + three + four + five + six + seven + eight

            # Perform the p-box permutation
            after_p_box = before_p_box.permute(p_box_permutation)

            R = L ^ after_p_box
            L = saved_R
        final = final + R + L

    a = final.get_text_from_bitvector()
    print()
    print("Encrypted text: ")
    print(a)
    print()

    FILEOUT.write(a)
    FILEOUT.close()

    return(a)





def decrypt(text, out_file, key):
    # Open out file

    length = len(text)

    strings = []
    low = 0
    high = 8


    while((length - 8) >= 0):       # Separate the text into strings of length 8 characters (bytes)
      strings.append(text[low:high])
      low = low + 8
      high = high + 8
      length = length - 8


    if(length != 0):     # Take care of any part of the string that was left over
        strings.append(text[high:])

    FILEOUT = open(out_file, 'w')

    final = BitVector(size = 0)

    for item in strings:

        bitvec = BitVector(textstring = item)


        [LE, RE] = bitvec.divide_into_two() # Split the BitVector in two


        round_key = extract_round_key(key) # Obtain the round keys


        for i in range(16):  # Start the 16 rounds of encrpytion / decryption

            saved_RE = RE

            expanded = RE.permute(expansion_permutation)

            expanded = expanded ^ round_key[15-i]

            # Divide the key in to 8 parts
            [one, five] = expanded.divide_into_two()
            [one, three] = one.divide_into_two()
            [one, two] = one.divide_into_two()
            [three, four] = three.divide_into_two()
            [five, seven] = five.divide_into_two()
            [five, six] = five.divide_into_two()
            [seven, eight] = seven.divide_into_two()

            # S-box substitution
            row=one.permute(row_perm).int_val()
            col=one.permute(col_perm).int_val()
            one = BitVector(intVal=s_box[0][row][col], size=4)

            # S-box substitution
            row=two.permute(row_perm).int_val()
            col=two.permute(col_perm).int_val()
            two = BitVector(intVal=s_box[1][row][col], size=4)

            # S-box substitution
            row=three.permute(row_perm).int_val()
            col=three.permute(col_perm).int_val()
            three = BitVector(intVal=s_box[2][row][col], size=4)

            # S-box substitution
            row=four.permute(row_perm).int_val()
            col=four.permute(col_perm).int_val()
            four = BitVector(intVal=s_box[3][row][col], size=4)

            # S-box substitution
            row=five.permute(row_perm).int_val()
            col=five.permute(col_perm).int_val()
            five = BitVector(intVal=s_box[4][row][col], size=4)

            # S-box substitution
            row=six.permute(row_perm).int_val()
            col=six.permute(col_perm).int_val()
            six = BitVector(intVal=s_box[5][row][col], size=4)

            # S-box substitution
            row=seven.permute(row_perm).int_val()
            col=seven.permute(col_perm).int_val()
            seven = BitVector(intVal=s_box[6][row][col], size=4)

            # S-box substitution
            row=eight.permute(row_perm).int_val()
            col=eight.permute(col_perm).int_val()
            eight = BitVector(intVal=s_box[7][row][col], size=4)


            before_p_box = one + two + three + four + five + six + seven + eight    # Combine the eight keys


            after_p_box = before_p_box.permute(p_box_permutation)   # Perform the p-box permutation


            RE = LE ^ after_p_box   # Save the LE and RE values
            LE = saved_RE



        final = final + RE + LE # Concatenate the two sides to obtain the final key

    a = final.get_text_from_bitvector()

    print("Decrypted text: ")
    print(a)

    FILEOUT.write(a)
    FILEOUT.close()



#################################### main #######################################

def main():
    ## write code that prompts the user for the key
    ## and then invokes the functionality of your implementation

    key = get_encryption_key()
    #FILE OPERATIONS
    fin = input("Input plain text inut file: ")  # opens the input file in current directory
    fout_1 = input("Encrypted file: ")
    fout_2 = input("Decrypted file: ")

    #READING FROM FILE
#    data_input = fin.read()  # stores input file data
#     data_key = fkey.read()    # stores key

    des(fin,fout_1,fout_2,key)

if __name__ == "__main__":
    main()
