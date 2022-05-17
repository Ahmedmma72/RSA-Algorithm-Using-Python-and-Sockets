from http import client
import socket
import pickle
import Algorithms
import utils

#setup socket
HeaderSize = 10
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 3000)) #connects to the server




#setup algorithm
primeArray = utils.read_data('primes.txt')
(p,q) = Algorithms.generate_two_prime_numbers(primeArray)
(e,d,n) = Algorithms.RSA_key_generator(p,q)        

#first send public key to server
publicKey = (e,n)
publicKey = pickle.dumps(publicKey) 
publicKey = bytes(f'{len(publicKey):<{HeaderSize}}', "utf-8") + publicKey # :< means left align
client_socket.send(publicKey)

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
