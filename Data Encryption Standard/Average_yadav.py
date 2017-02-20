#!/usr/bin/env python3


import sys
from DES_yadav import *


# Main Block
def main():

    # Inputs
    key = get_encryption_key()
    in_file = input("Input file with plaintext: ")
    en_file = input("Encrypted Output file: ")
    out_file = input("Plaintext Output file: ")

    # Call the helper functions
    diffusion(key, en_file)
    confusion(in_file, en_file)



if __name__ == "__main__":
    main()
