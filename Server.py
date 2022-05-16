import socket
import pickle
import Algorithms
import utils

#setup socket
HeaderSize = 10
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 3000))
serverSocket.listen(1)

#setup algorithm
primeArray = utils.read_data('primes.txt')
(p,q) = Algorithms.generate_two_prime_numbers(primeArray)
(e,d,n) = Algorithms.RSA_key_generator(p,q)

while True:
    clientSocket, address = serverSocket.accept()
    #first send public key to client
    publicKey = (e,n)
    publicKey = pickle.dumps(publicKey)
    publicKey = bytes(f'{len(publicKey):<{HeaderSize}}', "utf-8") + publicKey
    clientSocket.send(publicKey)
    while True:
        msg = input("Enter a message: ")
        msg = Algorithms.Encrypt(msg,n,d)
        msg = pickle.dumps(msg)
        msg = bytes(f"{len(msg):<{HeaderSize}}", 'utf-8') + msg
        clientSocket.send(msg)


