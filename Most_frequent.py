def most_frequent(string):
    dict = {}
    list = []
    for k in string:
        a = string.count(k)
        dict[k] = str(a)

    for i,j in dict.items():
        list.append(str(j)+'='+i)

    list.sort(reverse = True)

    for i in list:
        i = i[-1::-1]
        print(i)

n=input("enter: ")
print(most_frequent(n))
