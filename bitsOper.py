def bitsDetect(byte_val): #определить, какие биты в байте равны 1
    result = list()
    a = 0x80
    i = 7
    while a >= 1:
        if byte_val/a >= 1: 
            result.append(i)
            byte_val -= a
        a = int(a/2)
        i -= 1
    return result
    
def bitsConvert (lst): #получить байт, в котором биты списка lst равны 1
    result = 0
    a = 0x80
    i = 7
    while i >= 0:
        if i in lst:
            result += a
        a = int(a/2)
        i -= 1
    return result
    
    
def twos_comp(val, bits):
    try:
        val = int(val.hex(),16)
    except:
        pass
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    val = round((val/256), 3)
    return val
    
    
def de_twos_comp(val,bits):
    if val < 0:
        d = abs(int(val//1))
        c = round(abs(val)%1,3)
        if c>0: d -= 1
        b1 = 255-d
        b2 = round(255-c/(1/256))
        val = (b1<<8) + b2 + 1
        val = int.to_bytes(val,int(bits/8),'big')
    else:
        val = round(val/(1/256))
        val = int.to_bytes(val,int(bits/8),'big')
    return val
    
    
def from_slope(val):
    val = val[0] + val[1]/256
    return round(val,4)
    
def to_slope(val):
    d = int(val//1)
    c = val%1
    val = bytes([d,int(c*256)])
    return val
