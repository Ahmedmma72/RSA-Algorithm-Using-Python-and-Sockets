import random
# import utils
from utils import *
from math import ceil
from Crypto.Util.number import getPrime

def Encrypt(message, n, e):
    cipher = ""
    noChar = getNumberOfChars(n)
    maxCipherLength = len(str(n-1)) 
    for i in range(0, len(message), noChar):
        blockToEncrypt = ConvertToInt(message[:noChar]) #indexing outofbounds works fine in python
        cipherdBlock = str(PowerMod(blockToEncrypt, e, n))
        if (len(cipherdBlock) < maxCipherLength):  #make sure all cipher blocks are the same length
            cipherdBlock = cipherdBlock.zfill(maxCipherLength)
        cipher += cipherdBlock
        message = message[noChar:]
    return cipher


def Decrypt(cipher,n, d):
    maxCipherLength = len(str(n-1)) 
    message = ""
    for i in range(0, len(cipher), maxCipherLength):
        blockToDecrypt = int(cipher[:maxCipherLength])
        message += ConvertToStr(PowerMod(blockToDecrypt, d, n))
        cipher = cipher[maxCipherLength:]
    return message


#implement RSA Algorithm to generate public and private key
def RSA_key_generator(p,q):
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2,phi-1)     #choose e randomly from 1 to phi
    while GCD(e,phi) != 1:
        e = random.randint(2,phi-1)
    d = InverseModulo(e,phi)
    return (e,d,n)        

#generate two random integers from the array of prime numbers
def generate_two_prime_numbers( prime_array , nBits =0 ):
    if(nBits == 0):
        p = random.choice(prime_array)
        q = random.choice(prime_array)
        while p == q:
            q = random.choice(prime_array)
    else :
        p = getPrime(nBits )
        q = getPrime(nBits )
        while p == q:
            q = random.choice(prime_array)
    return (p,q)