"""Exponent profile data calculator"""
from calendar import c
import math
def calcExp():
    print("The thickness of one monolayer is (nm): ", end='')
    d=float(input())
    print("The length of the penetration is (nm): ", end='')
    L=float(input())
    N=round(L/d)
    points=[]
    z=0
    while math.e**(-z/N)>0.01:
        points.append(math.e**(-z/L))
        print(z*d,math.e**(-z/N))
        z+=1

calcExp()