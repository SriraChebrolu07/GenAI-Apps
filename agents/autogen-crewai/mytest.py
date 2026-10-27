# l1=[1,2,3,3,4,4,5,]
# l2=[2,3,5,6,7,8,9]

# a=l1+l2
# print(a)
# b=set(a)
# print(b)
# c=list(b)
# print(c)



# a="morning"
# rev=" "

# for i in a:
#   rev=i+rev
# print(rev)



# def reverse(x):
#    reverse=" "

#    for i in x:
#       reverse = i + reverse
#    print(reverse)

#    return reverse

# reverse("sriram")




# class classA:
#    print("This is classA")
#    def display(self):
#       a=5
#       b=4
#       print(a,b)

#display(self)

# obj=classA()
# obj.display()

# class classB(classA):
#    print("this is calss B")
# obj=classB()
# obj.display()





# a="554"
# b=float(a)
# print(b)


# a= range(1,10)
# for i in a:
#     print(i)





# class grand():
#     def fun1(self):
#         print("this is grand parent class")
# # obj=grand()
# # obj.fun1()

# class parent(grand):
#     def fun2(self):
#         print("this is parent class")
# obj2=parent()
# # obj2.fun2()
# # obj2.fun1()

# class child(parent):
#     def fun3(self):
#         print("this is grand child class")
# obj3=child()
# # obj3.fun3()
# # obj3.fun2()
# # obj3.fun1()




# d={"a":"sr",2:"ae"}

# print(d["a"])

# print(d.items())
# print(d.values())
# print(d.keys())

# d["a"]="as"
# print(d)


word =input("enter your string\n").lower()
word=word.replace(" ","")
rev=""

for i in word:
    rev=i+rev

print(rev)

if rev==word:
    print("its a palindrome")
else:
    print("not a palindrome")