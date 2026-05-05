def sumarDigitosMultiplos(n, m):
    res = 0
    n1 = 0
    while n>0:
        n1 = n%10
        if n1%m == 0:
            res += n1 
        n //= 10 
    return res 
