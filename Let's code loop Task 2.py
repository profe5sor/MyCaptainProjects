a = list(map(int,input().split()))
b = []
c=len(a)
for i in range(c):
    if a[i]>=0:
        b.append(a[i])

print(b)
