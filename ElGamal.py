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
    a = primRoot(p)
    
    private = random.randint(1, p-2)
    public = pow(a,private,p)
    return p, a, private, public


""" Signature Generation 
"""
def egGen(p, a, x, message):
    while 1:
        k = random.randint(1,p-2)
        if gcd(k, p-1)==1: break
    r = pow(a,k,p)
    l = modinv(k, p-1)
    
    #cipher = [pow(ord(char),key,n) for char in plaintext]
    s = [l*(ord(char) - x*r)%(p-1) for char in message]
    return r,s


""" Signature Verification 
"""
def egVer(p, a,	y, r, s, message):
    if r < 1 or r > p-1 : return False
    v1 = [pow(y,r,p)%p * pow(r,num,p)%p for num in s]
    #print(v1)
        
    hashed = hashFunction(message)
    v2 = [pow(a,ord(char),p) for char in hashed]
    #print(v2)

    isValid = v1==v2
    
    if isValid:
        print("Verification successful: ", )
        print(v1, " = ", v2)
    else:
        print("Verification failed:")
        print(v1, " != ", v2)


def main():
    message = "36jkkk"
    print("Message: ", message)
    hashed = hashFunction(message)
    print("Hashed version: ", hashed)
    
    prime,alpha,private,public = egKey()    
    print ("prime,alpha,private,public", prime,alpha,private,public)
    rr,ss = egGen(prime,alpha,private, hashed)
      
    print("rr,ss", rr, ss)
    egVer(prime, alpha, public, rr, ss, message)
      
main()  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 