def compute_square(r):
    return r * r

def cone_volume(r, h):
    return (0.33) * 3.14 * compute_square(r) * h

cone_vol = cone_volume(2, 4)    
print(cone_vol)