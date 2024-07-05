#1
print(123==123,end = " ")
print('gh')
True # 123 is 123 so True, but end = " " is not working so just True presented ,
     # and just variable end was defined
print(123<123)
False # 123 is just 123 , so 123 is not smaller than 123 , so False

#2
for i in range(2,5):
    print(i)
2
3
4
# range(2,5) meaning is 2,3,4 , because 5 is not operated

#3
for i in range(10,11):
    print(i)
10
# range(10,11) meaning is 10 , because 11 is not operated

#4
for k in range(10,5,-2):
    print(k)
10
8
6
# range(10,5,-2) meaning 10, 8, 6 , because step value -2, so 10, 8, 6, 4, but last condition is 6, so 10, 8, 6
#5
i = 5
for a in range(3):
    print(i)
    i = i -1
5
4
3
# range(3) meaning is 0, 1,2 , initial value i is 5, in for sentecne,
# i = i -1 menaing i -1 and put that value to i
# for example 1st step, i is 5, a is 0, print(i) present 5, i was exchange to 4 , because i -1 =3
# 2nd step  i is 4, a is 1, print(i) present 4, i was exchange to 3 , because i -1 is 3
# 3rd step  i is 3, a is 2, print(i) present 3, i was exchange to 2 , because i -1 is 2
# this for loop end
#6
a = [1,2,3]
for i in a:
    print(i)
1
2
3
# a means 1,2,3 sequence , 1st step i is 1, so print(i) present 1
# 2nd step step i is 2, so print(i) present 2
# 3rd step step i is 3, so print(i) present 3

