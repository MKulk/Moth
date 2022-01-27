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
    print("The saturation magnetisation of the reference material is: ", end='')
    Mref=float(input())
    print("The saturation magnetisation of the neighbouring material is: ", end='')
    M2=float(input())
    print("The internal exchange of the reference material is: ", end='')
    Jinternal=float(input())
    print("The ratio of the interlayer exchange and intralayer exchange is (in %): ", end='')
    n=float(input())
    Jinterlayer=Jinternal*Mref*n/(100*M2)
    print("")
    print("Jinterlayer={}".format(Jinterlayer))
            
        


if __name__=="__main__":
    converter()