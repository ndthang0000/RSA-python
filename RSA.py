
# import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randrange, getrandbits
import uuid

def power(a,d,n):
  ans=1
  while d!=0:
    if d%2==1:
      ans=((ans%n)*(a%n))%n
    a=((a%n)*(a%n))%n
    d>>=1
  return ans


def MillerRabin(N,m):
  #m*(2^r)=N-1
  #genarate radom "a"
  a = randrange(2, N - 1)
  x=power(a,m,N)            
  if x==1 or x==N-1:
    return True       #its a non square root
  else:
    while(m!=N-1):
      x=((x%N)*(x%N))%N   #pow(x,2,N)
      if x==1:
        return False
      if x==N-1:
        return True  
      m<<=1              # we'll shift until m reach n-1 ( r times)
  return False


def PrimeTest(N,K):  #FERMAT TEST
  # n is number to test, K is how many time we test

  if N==3 or N==2:
    return True
  if N<=1 or N%2==0:
    return False
  
  #Step2: Find r odd M :
  # 	+Find m : m*(2^r)=N-1
  #   +we will minimum m by shift right as much as possible ( r times ) 
  m=N-1
  while m%2!=0:
    m/=2             #rightshift
  
  #STep 3:
  # call MILLerRabin to check nontrivial square K time(the reason is this funcion will genarate a radom "a")
  # for more: https://vi.wikipedia.org/wiki/Ki%E1%BB%83m_tra_Miller-Rabin
  # + In  Mill m will shift left until m = n-1 ( r times )
  for _ in range(K):
    if not MillerRabin(N,m):
      return False
  
  #step4:
  return True
  

def generate_prime_candidate(length):
  # generate random bits
  p = getrandbits(length)

  # apply a mask to set MSB and LSB to 1
  # Set MSB(<<shift left) to 1 to make sure we have a Number of 1024 bits.
  # Set LSB(Last bit) to 1 to make sure we get a Odd Number.
  p |= (1 << length - 1) | 1
  return p



def generatePrimeNumber(length):
  A=4
  #because we generate randome number A with "lenght" bits , so we dont know if
  #A is prime or not , that why we need to check
  #128 is number test of MILLer-rabin, read function PrimeTest for more
  while not PrimeTest(A, 128):  
        A = generate_prime_candidate(length)
  return A


 
def GCD(a,b):
  if a==0:
    return b
  return GCD(b%a,a)


#Finding D: It must satisfies this property:-  (D*E)Mod(eulerTotient)=1;
#Now we have two Choices
# 1. That we randomly choose D and check which condition is satisfying above condition.
# 2. For Finding D we can Use Extended Euclidean Algorithm: ax+by=1 i.e., eulerTotient(x)+E(y)=GCD(eulerTotient,e)
#Here, Best approach is to go for option 2.( Extended Euclidean Algorithm.)

def Bezout(E,eulerTotient):   #gcdExtended   
  a1,a2,b1,b2,d1,d2=1,0,0,1,eulerTotient,E

  while d2!=1:

    # k
    k=(d1//d2) #the floor division // rounds the result down to the nearest whole number

    #a
    temp=a2
    a2=a1-(a2*k)
    a1=temp

    #b
    temp=b2
    b2=b1-(b2*k)
    b1=temp

    #d
    temp=d2
    d2=d1-(d2*k)
    d1=temp

    D=b2

  if D>eulerTotient:
    D=D%eulerTotient
  elif D<0:
    D=D+eulerTotient

  return D



def encode(text):
  s=''
  for char in text:
    
    o=str(ord(char))
    #print(o)
    s+=o
  dec = int(s)
  return dec


def encryption(text,e,n):

  #x=np.zeros(shape=[ord(char)], dtype=np.uint8)
  #x=np.uint8(ord(char))
  encoded=encode(text)
  changetype=encoded
  result = pow(changetype,e,n)
  return result

def decode(code):
  stringified= str(code)
  string=''
  i=0
  while i<len(stringified):
    num= int(stringified[i:i+2])
    #print(num)
    if num<=30 :
      string+= chr(int(stringified[i:i+3]))
      #print(num," => ",string)
      i+=3
    else:
      string+= chr(int(num))
      #print(num," => ",string)
      i+=2
  return string

def decryption(encypted,d,n):
  
  return pow(encypted,d,n)

#-----------------------------------------

# text=str(uuid.uuid1()).split('-')[0] +'theone'
# print(type(text))
# print(text)
# text='4196b7a8theone'
# e=65537
# d=19068282114638889730511490438900113
# n=485468956275981451548133459248763171


# res=encryption(text,'65537','19068282114638889730511490438900113')
# print("encrypted: ",res)
# decrypted= decryption(res,19068282114638889730511490438900113,485468956275981451548133459248763171)
# print("Decrypted: ",decrypted)
# decoded=decode(decrypted)
# print("Decoded: ",decoded)
# print(type(decoded))






# #-----------------------------------------------------------
# #Let check

# print("Start step 1")
# # STEP 1: Generate Two Large Prime Numbers (p,q) randomly
# length=5
# P=generatePrimeNumber(length)
# Q=generatePrimeNumber(length)
# print(P)
# print(Q)

# print("Start step 2")
# #Step 2: Calculate N=P*Q and Euler Totient Function (phi) = (P-1)*(Q-1)
# N=P*Q
# eulerTotient=(P-1)*(Q-1)
# print(N)
# print(eulerTotient)

# print("Start step 3")
# #Step 3: Find E such that GCD(E,eulerTotient)=1(i.e., e should be co-prime): E.D mod φ = 1 
# E=int(generatePrimeNumber(4))

# while GCD(E,eulerTotient)!=1:
#   E=int(generatePrimeNumber(4))
# print(E)

# print("Start step 4")
# # Step 4: Find D.
# D=Bezout(E,eulerTotient)
# print(D)

# #image stuffs
# # my_img = cv2.imread('D:/Pictures/hakuna.jpg')
# # cv2.imshow("the originals",my_img)
# # cv2.waitKey(0)

# # row,col=my_img.shape[0],my_img.shape[1]
# # print("row:  ",row)
# # print("col: ",col)
# my_img= "123456789thang123"
# print("Start step 5")
#Step 5: Encryption 

# ciphertext=encryption(my_img)
# str
# print("Encrypted Text: ",''.join(str(ciphertext)))

# print("Start step 6")
# # Step 6: Decryption
# #dec_img=decryption(ciphertext)
# #print(dec_img)
# # cv2.imshow("decrypt",dec_img)
# # cv2.waitKey(0)

# n="13120416944641884087579239747959973773026172162107438181491151619298277205689104266779946368998802035269648407601700218684052732790424669289128955099781145482165594258828885909644265967735953482056099871111540985960613852271814937302439062"
# n=131204169446418840875792397479599737730261721621074381814911516192982772056891042667799463689988020352696484076017002186840527327904246692891289550997811454821655942588288859096442659677359534820560998711115409859606138522718149373024390622114075371683937393132448487644864480468349226497414765184060868134617
# print(power(n,D,N))
# #print(len(n))