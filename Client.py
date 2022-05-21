from http import client
import socket
import pickle
import Algorithms
from utils import *
import random
from Crypto.Util.number import getPrime

#setup socket
HeaderSize = 10
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 3000)) #connects to the server

#choose mode of operation
print("Welcome to the client!")
print("1) Normal (Keys are auto generated)\n2) testing(You get to insert key parameters)\n")
mode = input("Enter Your Choice: ")
while(mode != "1" and mode != "2"):
    print("Invalid Choice!")
    mode = input("Enter Your Choice: ")
#setup algorithm
# primeArray = read_data('primes.txt')
if(mode == "1"):
    keySize = int(input("Enter Key Size: ")) 
    while(True):
        if(keySize < 0)     : print('key size cant be negative')
        elif(keySize < 30)  : print('please insert bigger key size')
        elif(keySize > 1500)  : print('max key size = 1500')
        else :     break
        keySize = int(input("Enter Key Size: ")) 
    (p,q) = Algorithms.generate_two_prime_numbers( keySize // 2)
    (e,d,n) = Algorithms.RSA_key_generator(p,q)
else:
    p = int(input("Enter p: "))
    while(isPrime(p) == False):
        print("P must be PRIME!")
        p = int(input("Enter p: ")) 
    print("want to insert q y/n")
    choice = input("Enter Your Choice: ")
    while(choice != "y" and choice != "n"):
        print("Invalid Choice ! ")
        choice = input("Enter Your Choice: ")
    if(choice == "y"):    
        q = int(input("Enter q: "))
        while(isPrime(q) == False or p*q < 256):
            print("q must be PRIME and p*q must be greater than 255!")
            q = int(input("Enter q: "))
    else:
        # q = random.choice(primeArray)
        q = getPrime(512)
        while(p*q <255):
            # q = random.choice(primeArray)
            q = getPrime(512)
        print("generated q :" , q)    
    n = p*q    
    print("want to insert e y/n")
    choice = input("Enter Your Choice: ")
    while(choice != "y" and choice != "n"):
        print("Invalid Choice ! ")
        choice = input("Enter Your Choice: ")
    if(choice == "y"):
        e = int(input("Enter e: "))
        while(GCD(e,(p-1)*(q-1)) != 1 or e <= 1 or e >= (p-1)*(q-1)):
            print("e must be greater than 1 ,smaller than (p-1)*(q-1) ,and coprime to (p-1)*(q-1)!")
            e = int(input("Enter e: "))
    else:
        phi = (p-1)*(q-1)
        e = random.randint(2, phi-1)  # choose e randomly from 1 to phi
        while GCD(e, phi) != 1:
            e = random.randint(2, phi-1)
        print("chosen e: ", e)    
    d = InverseModulo(e,(p-1)*(q-1))    

#first send public key to server
publicKey = (e,n)
publicKey = pickle.dumps(publicKey) 
publicKey = bytes(f'{len(publicKey):<{HeaderSize}}', "utf-8") + publicKey # :< means left align
client_socket.send(publicKey)

print("ready to recieve message")
#variables for recieving messages
full_msg = b''
new_msg  = True
msg_len = 0

while True:
    msg = client_socket.recv(16)
    if new_msg:
        msg_len = int(msg[:HeaderSize])
        new_msg = False  
    full_msg += msg
    if len(full_msg)-HeaderSize == msg_len:
        msg = pickle.loads(full_msg[HeaderSize:])
        decryptedMsg = Algorithms.Decrypt(msg,n,d)
        print('\n------------- ')
        print(rf"decrypted Msg {msg}" , '\n')
        print(f"recieved message: {decryptedMsg}")
        new_msg = True
        full_msg = b''
