# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 22:22:15 2021

@author: Phillip Dix
"""

from itertools import repeat
from functools import reduce
from operator import mul
from math import factorial
from sympy import Rational

from numpy import array,flip
#no performance gain from using numpy arrays, just here for syntactic sugar

def stack(A,n):
    return list(repeat(A,n))

def zerocube(n):
    return stack(stack(stack(Rational(0),n),n),n)

def e26(m,k,e1,e2,e3):
    #e1 = a[m-2,m-1,k]
    #e2 = a[m-1,m,k-1]
    #e3 = a[m-2,m,k-1]
    return (1/((m-1)*(m-k)))*(m*e1 - k*(m-1)*e2 - e3)

def e27(m,k,i,e1,e2):
    #e1 = a[i+1,m,k]
    #e2 = a[i,m-1,k]
    return (m/(i+1-m))*((i+1)*e1-e2)

def e29_term(i,j,m,k,e1):
    #e1 = a[i+j,m,k]
    return reduce(mul,range(i+1,i+j+1),1)*e1*m**i

def mr(a):
    return map(Rational,a)

def CardinalSplineCalculations(order):
    a = array(zerocube(order+1))
    a[0,1,0] = Rational(1)
    for m in mr(range(2,order+1)):
        g = Rational(int(m/2) - 1)
        for k in mr(range(0,g+1)):
            a[m-1,m,k] = e26(m,k,a[m-2,m-1,k],a[m-1,m,k-1],a[m-2,m,k-1])
            a[m-1,m,m-k-1] = ((-1)**(m-1))*a[m-1,m,k]
            for i in mr(range(m-2,-1,-1)):
                a[i,m,k] = e27(m,k,i,a[i+1,m,k],a[i,m-1,k])
                a[i,m,m-k-1] = (((-1)**i)/factorial(i))*sum([e29_term(h,i,m,k,a[i+h,m,k]) for h in mr(range(0,m-i))])
        if m % 2 != 0:
            a[m-1,m,g+1] = e26(m,g+1,a[m-2,m-1,g+1],a[m-1,m,g+1-1],a[m-2,m,g+1-1])
        for i in mr(range(m-2,-1,-1)):
            a[i,m,g+1] = e27(m,g+1,i,a[i+1,m,g+1],a[i,m-1,g+1])
    return a

def CardinalSplineMatrix(order):
    return flip(CardinalSplineCalculations(order)[:-1,-1,:-1].transpose(),1)

def ScaledSplineMatrix(order):
    from sympy import Symbol,Matrix,poly,expand
    #This paper returns the correct coefficients, but they're more convenient 
    #for my use when scaled differently, in particular I use the form:
    #
    #                                         [P0]                                       
    #                                         [P1]                                      
    #  [1 t t**2 t**3 ... t**n] * (1/c) * B * [P2]                                      
    #                                         [...]                         
    #                                         [Pn]             
    #
    # such that t is the parameter in [0,1], B is the matrix I want, and Pn 
    # are the control points.  This function is my shortcut to get what I 
    # need to use directly in this equation
    t = Symbol('t')
    T = [t**i for i in reversed(range(0,n))]
    polynomials = Matrix(CardinalSplineMatrix(n)) * Matrix(T)
    scaled_polynomials = [poly(expand(i.subs(t,t+j)),t) for j,i in enumerate(polynomials)]
    const_coeff = poly(polynomials[0]).all_coeffs()[0]
    return (flip(array([[j/const_coeff for j in poly(i,t).all_coeffs()] for i in scaled_polynomials])).transpose(),Rational(const_coeff))

if __name__ == '__main__':
    n = 13
    print(CardinalSplineMatrix(n))
    B,const = ScaledSplineMatrix(n)
    print(B)
    print(const)