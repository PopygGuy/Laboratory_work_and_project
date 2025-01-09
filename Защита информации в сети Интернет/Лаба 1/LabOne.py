s1 = 1
s2 = 1

def modmult(a, b, c, m, s):
    global q
    q = s // a
    s = b * (s - a * q) - c * q
    if s < 0:
        s += m
    return s

def comb_lcg():
    global s1, s2
    s1 = modmult(53668, 40014, 12211, 2147483563, s1)
    s2 = modmult(52774, 40692, 3791, 2147483399, s2)
    
    z = s1 - s2
    if z < 1:
        z += 2147483562
        
    return z * 4.656613e-10

def init_lcg(init_s1, init_s2):
    global s1, s2
    if not (1 <= init_s1 <= 2147483562):
        raise ValueError("s1 должен быть в диапазоне [1, 2147483562]")
    if not (1 <= init_s2 <= 2147483398):
        raise ValueError("s2 должен быть в диапазоне [1, 2147483398]")
    
    s1 = init_s1
    s2 = init_s2

# Пример использования
init_lcg(1, 33333)
random_value = comb_lcg()
print(random_value)