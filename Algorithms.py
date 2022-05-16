import random
import utils
from math import ceil

def Encrypt(message, n, e):
    cipher = ""
    noChar = utils.getNumberOfChars(n)
    maxCipherLength = len(str(n-1)) 
    for i in range(0, len(message), noChar):
        blockToEncrypt = utils.ConvertToInt(message[:noChar]) #indexing outofbounds works fine in python
        cipherdBlock = str(utils.PowerMod(blockToEncrypt, e, n))
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
        message += utils.ConvertToStr(utils.PowerMod(blockToDecrypt, d, n))
        cipher = cipher[maxCipherLength:]
    return message


#implement RSA Algorithm to generate public and private key
def RSA_key_generator(p,q):
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2,phi-1)     #choose e randomly from 1 to phi
    while utils.GCD(e,phi) != 1:
        e = random.randint(2,phi-1)
    d = utils.InverseModulo(e,phi)
    return (e,d,n)        

#generate two random integers from the array of prime numbers
def generate_two_prime_numbers(prime_array):
    p = random.choice(prime_array)
    q = random.choice(prime_array)
    while p == q:
        q = random.choice(prime_array)
    return (p,q)    