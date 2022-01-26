import math
def converter():
    print("""
          +---------------------------------------------------------------------+
          |                                                                     |
          |                    Exchange calculation script                      |
          |                   Mykola Kulyk, KTH, 26.01.2022                     |
          |                 This script calculates the value of                 |    
          |         weak interlayer interaction as a fraction of the            |
          |      intralayer exchange interaction of the reference material      |
          +---------------------------------------------------------------------+
        """)
    print("The saturation magnetisation of the reference material is:")
    Mref=float(input())
    print("The saturation magnetisation of the neighbouring material is:")
    M2=float(input())
    print("The internal exchange of the reference material is:")
    Jinternal=float(input())
    print("The length (in monolayers) of the extemded decay is: (0 if the long range interaction is disabled)")
    L=float(input())
    print("The ratio of the interlayer exchange and intralayer exchange is: (in %)")
    n=float(input())
    if L==0.0:
        Jinterlayer=Jinternal*Mref*n/(100*M2)
    else:
        points=[]
        z=0
        while math.e**(-z/L)>0.01:
            points.append(math.e**(-z/L))
            print(z,math.e**(-z/L))
            z+=1
            
        


if __name__=="__main__":
    converter()