list1=[1,2,2,3,4,1,5]
ll=0
for in1, li1 in enumerate(list1):
    for in2, li2 in enumerate(list1):
        if in1-ll>=in2:
            pass
        else:
            if li1==li2:
                list1.pop(in1)
                ll=ll+1
print(list1)