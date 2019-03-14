def f(s1,s2):
    k  = 0
    for i in range(0,len(s1)):
        if s1.find(s2,i,len(s1)-len(s2)):
            k += 1
    return k
print(f('ABCDCDC','CDC'))