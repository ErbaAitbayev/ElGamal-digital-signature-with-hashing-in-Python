import random
from hashlib import sha256

def hashFunction(message):
    hashed = sha256(message.encode("UTF-8")).hexdigest()
    return hashed
    
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


#Euclid's extended algorithm for finding the multiplicative inverse of two numbers    
def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise Exception('Modular inverse does not exist')
	return x % m    
 
 
def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a


def primRoot(modulo):
    roots = []
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            roots.append(g)           
    return roots[0]
 

def egKey():
    p = 17
    g = primRoot(p)
    
    privateKey = random.randint(1, p-2)
    publicKey = pow(g,privateKey,p)
    return p, g, privateKey, publicKey


""" Signature Generation 
"""
def egGen(p, g, x, message):
    while 1:
        k = random.randint(1,p-2)
        if gcd(k, p-1)==1: break
    r = pow(g,k,p)
    l = modinv(k, p-1)
    
    s = [l*(ord(char) - x*r)%(p-1) for char in message]
    return r,s


""" Signature Verification 
"""
def egVer(p, a,	y, r, s, message):
    if r < 1 or r > p-1 : return False
    v1 = [pow(y,r,p)%p * pow(r,num,p)%p for num in s]
        
    hashed = hashFunction(message)
    v2 = [pow(a,ord(char),p) for char in hashed]


    isValid = v1==v2
    
    if isValid:
        print("Verification successful: ", )
        print(v1, " = ", v2)
    else:
        print("Verification failed:")
        print(v1, " != ", v2)


def main():
    message = "AaaBbbCccDddEeeFff12345678910"
    print("Message: ", message)
    hashed = hashFunction(message)
    print("Hashed version: ", hashed)
    print()
    
    p, g, private, public = egKey() 
    print("Public key (p, g, y): ", [p, g, public])
    print("Private key (x): ", private)
    
    print()
    rr,ss = egGen(p,g,private, hashed)    
    print("Signature (r, s): ", rr, ss)
    
    print()
    egVer(p, g, public, rr, ss, message)
      
main()  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
