from http import client
import socket
import pickle
import Algorithms
import utils

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
if(mode == "1"):
    primeArray = utils.read_data('primes.txt')
    (p,q) = Algorithms.generate_two_prime_numbers(primeArray)
    (e,d,n) = Algorithms.RSA_key_generator(p,q)
else:
    p = int(input("Enter p: "))
    while(utils.isPrime(p) == False):
        print("P must be PRIME!")
        p = int(input("Enter p: "))
    q = int(input("Enter q: "))
    while(utils.isPrime(q) == False or p*q < 256):
        print("q must be PRIME and p*q must be greater than 255!")
        q = int(input("Enter q: "))
    n = p*q    
    e = int(input("Enter e: "))
    while(utils.GCD(e,(p-1)*(q-1)) != 1 or e < 1 or e > (p-1)*(q-1)):
        print("e must be greater than 1 ,smaller than (p-1)*(q-1) ,and coprime to (p-1)*(q-1)!")
        e = int(input("Enter e: "))
    d = utils.InverseModulo(e,(p-1)*(q-1))    
          

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
        msg = Algorithms.Decrypt(msg,n,d)
        print("recieved message: ",msg)
        new_msg = True
        full_msg = b''
