import socket
import pickle
import Algorithms
import utils

#setup socket
HeaderSize = 10 #so the length of largest message is 99..9 10 times (pretty big i guess)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #fist param is address family, second is socket type
serverSocket.bind((socket.gethostname(), 3000)) #binds the socket to the port
serverSocket.listen(1) #listens for 1 connection

#varaibles to recieve public key
full_msg = b''
new_msg  = True
msg_len = 0
e = 0
n = 0

while True:
    clientSocket, address = serverSocket.accept()
    #reciver public key from client
    pkRecieved = False
    while not pkRecieved:
        msg = clientSocket.recv(HeaderSize)
        if new_msg:
            msg_len = int(msg[:HeaderSize])
            new_msg = False
        full_msg += msg
        if len(full_msg)-HeaderSize == msg_len:
            msg = pickle.loads(full_msg[HeaderSize:])
            (e,n) = msg
            pkRecieved = True

    print("Public key recieved : ..." )    
    print(f"e = {e} \n\n" )    
    print(f"n =  {n}  \n\n------------" )    
    while True:
        msg = input("Enter a message: ")
        msg = Algorithms.Encrypt(msg,n,e)
        msg = pickle.dumps(msg) #converts to bytes
        msg = bytes(f"{len(msg):<{HeaderSize}}", 'utf-8') + msg
        clientSocket.send(msg)


