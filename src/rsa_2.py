
import cv2
import numpy as np

from random import randrange, getrandbits


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


#Finish basic things from RSA
==upload anh===
- Clien gửi public key RSA lên cho server 
- server generate 1 key AES(lưu key này vào database) đc mã hóa bằng key public RSA  rồi gửi cho client 
- client lấy key AES nhận đc từ server để mã hóa ảnh, rồi gửi ảnh đã encrypt bằng key AES đó lên cho server lưu trữ

===get ảnh===
- Clien gửi public key RSA lên cho server
- Server đọc database lấy ra key AES rồi mã hóa bằng RSA(mới nhận) rồi gửi ảnh (đã mã hóa bằng AES) và key AES(mã hóa bằng RSA)
- Client nhận Anh(encrypt) và key AES(encrypt), rồi giải mã để lấy key AES 
- rồi dùng key AES đã giải mã ảnh 


====chia sẽ ảnh=====
- chủ sở hữa ảnh gửi yêu cầu chia sẽ lên server, Server sẽ sử dụng key AES trong database 
- Thực hiện các bước tương tự như get ảnh

#Now handle image stuffs :>>
#color picture : RBG
def encryption(my_img):
  row,col=my_img.shape[0],my_img.shape[1]
  enc = [[0 for x in range(col)] for y in range(row)]
  for i in range(0,row):
    for j in range(0,col):
      r,b,g=my_img[i,j]
      r_en=power(r,E,N)
      b_en=power(b,E,N)
      g_en=power(g,E,N)
      enc[i][j]=[r_en,b_en,g_en]
  #     #show encrypt picture
  #     r_en=r_en%256
  #     b_en=b_en%256
  #     g_en=g_en%256
  #     my_img[i,j]=[r_en,b_en,g_en]
  # cv2.imshow("decrypt",my_img)
  # cv2.waitKey(0)
  return enc

def show_EncryptImage(enc):
  row = len(enc)
  col = len(enc[0])
  #print(row)
  #print(col)
  blank_image = np.zeros(shape=[row, col, 3], dtype=np.uint8)
  for i in range(0,row):
    for j in range(0,col):
      r,b,g=enc[i][j]
      r=r%256
      b=b%256
      g=g%256
      blank_image[i,j]=[r,b,g]
  #return enc_img
  cv2.imshow("encrypt",blank_image)
  cv2.imwrite("encrypt.jpg",blank_image)
  cv2.waitKey(0)



def decryption(enc):
  row = len(enc)
  col = len(enc[0])
  my_img = np.zeros(shape=[row, col,3], dtype=np.uint8)
  for i in range(0,row):
    for j in range(0,col):
      r,b,g=enc[i][j]
      r_de=power(r,D,N)
      b_de=power(b,D,N)
      g_de=power(g,D,N)
      my_img[i,j]=[r_de,b_de,g_de] 
  return my_img



#-----------------------------------------------------------
#Let check

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
# E=generatePrimeNumber(4)

# while GCD(E,eulerTotient)!=1:
#   E=generatePrimeNumber(4)
# print(E)

# print("Start step 4")
# # Step 4: Find D.
# D=Bezout(E,eulerTotient)
# print(D)

# #image stuffs
# my_img = cv2.imread('D:/Pictures/hakuna.jpg')
# cv2.imshow("the originals",my_img)
# cv2.waitKey(0)

# row,col=my_img.shape[0],my_img.shape[1]
# print("row:  ",row)
# print("col: ",col)

# print("Start step 5")
# #Step 5: Encryption 
# enc=encryption(my_img)
# show_EncryptImage(enc)

# print("Start step 6")
# #Step 6: Decryption
# dec_img=decryption(enc)
# cv2.imshow("decrypt",dec_img)
# cv2.waitKey(0)