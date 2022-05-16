import socket
import pickle
import Algorithms

#setup socket
HeaderSize = 10
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 3000))


full_msg = b''
new_msg  = True
msg_len = 0

#receive public key from server
pkRecieved = False
while not pkRecieved:
    msg = s.recv(16)
    if new_msg:
        msg_len = int(msg[:HeaderSize])
        new_msg = False  
    full_msg += msg
    if len(full_msg)-HeaderSize == msg_len:
        msg = pickle.loads(full_msg[HeaderSize:])
        (e,n) = msg
        new_msg = True
        full_msg = b''
        pkRecieved = True

print("Public key recieved")
while True:
    msg = s.recv(16)
    if new_msg:
        msg_len = int(msg[:HeaderSize])
        new_msg = False  
    full_msg += msg
    if len(full_msg)-HeaderSize == msg_len:
        msg = pickle.loads(full_msg[HeaderSize:])
        msg = Algorithms.Decrypt(msg,n,e)
        print("recieved message: ",msg)
        new_msg = True
        full_msg = b''
