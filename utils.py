#reads data from text file
def read_data(file_name):
    array = []
    with open(file_name, 'r') as fobj:
        for line in fobj:
            row = [int(num) for num in line.split()]
            array +=row
    return array

#function to reverse a string
def Reverse(str):
    string = ""
    return string.join(reversed(str))


#convert string to int 
def ConvertToInt(message):
  result = 0
  for char in message:
    result *= 256       #there are 256 characters in the ascii table
    result += ord(char) #ord() returns the ascii value of the character
  return result

#convert int to string
def ConvertToStr(message):
    result = ""
    while message > 0:
        result += chr(message % 256) #chr() returns the character of the ascii value
        message //= 256              #get the next character
    return Reverse(result) #reverse the string  

#return greatest common divisor of two numbers
def GCD(a, b):
  if b == 0:
    return a
  return GCD(b, a % b)    

#return the gcd along with the coefficent of bezout's identity
def ExtendedEuclid(a, b):
    if b == 0:
        return (a, 1, 0)
    (gcd, x1, y1) = ExtendedEuclid(b, a % b)
    return (gcd, y1, x1 - (a // b) * y1)

#return the inverse modulo of a number using the extended euclid identity
def InverseModulo(a, n):
    (gcd ,x1, y1) = ExtendedEuclid(a, n)
    if gcd != 1:
        return None # inverse doesn't exist
    else:
        if x1 < 0:
            x1 = (x1 % n + n) % n  #account for negative numbers
    return x1

#retun aaaa...a (b times) modulo n 
#works for large numbers (algorithm taken from Cryptography and Network Security by william stallings)
def PowerMod(a,b,n):
    b = bin(b)[2:]
    f = 1
    for i in b:
        f = (f*f)%n
        if i == '1':
            f = (f*a) % n
    return f

#function to calculate how many chars can be encrypted by a given key and the length of the equivalent ciphertext
def getNumberOfChars(key):
    noChar = 0
    key = key //256
    while(key > 0):
        noChar += 1
        key = key // 256
    return noChar