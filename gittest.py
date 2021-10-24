print('Hello, world')
print('I check local commit task')
print('I check local commit task2')
print('I check local commit task3')
print('I check local commit task4')

x = 0

bool(0)
bool((None))
bool([0])
bool((0))

print('a','b','c', sep='')
print('a' + 'b' + 'c')

for n in range(11):
    if(n%2) !=0:
        continue
    print(n, end=' ')

print('a'*2)

age =1
++age

g = (4,5,4,6)
h ={4,5,6,4}
g.append(66)

# 시스템 확인 하는 문구
from sys import platform
platform
platform
if platform == "linux" or platform == "linux2":
    print('linux')
elif platform == "darwin":
    print('osx') # mac
elif platform == "win32":
    print('windows')

# mac file finding and copying

import os
os.getcwd()
# os.listdir(path): return a list of then entries in the directory given by path
os.listdir(os.getcwd())

os.path.isfile('/Users/home/PycharmProjects/chromedriver')
os.path.isfile('')

'/Users/gwon-yonghwan/PycharmProjects/chromedriver'
'/Users/home/Downlodads'

import shutil
src_dir = '/Users/home/Downloads'
src_fname = 'chromedriver'
dst_dir = '/Users/home/PycharmProjects'
dst_fname = 'chromedriver2'
src = os.path.join(src_dir, src_fname)
dst = os.path.join(dst_dir, dst_fname)
shutil.copy(src, dst)
executable_path = '/Users/home/PycharmProjects/chromedriver2'
