#coding:utf-8
somelist = ['a','b','c','d','e','f','g','h']
print somelist[:]
print somelist[3:]
print somelist[3:5]
print somelist[3:-1]
print somelist[3:-2]
print somelist[-3:]
print somelist[-3:-1]
print somelist[-0:]
print somelist[0:]

print somelist[::-1]
print somelist[::2]
print somelist[1::2]
print somelist[::-2]

"""列表迭代,并取下标"""
for num,iter in enumerate(somelist):
    print '{0}:{1}'.format(num,iter)

for i in range(len(somelist)):
    print '{0}:{1}'.format(i,somelist[i])

"""数组是否为空判断"""
if somelist:
    print True
else:
    print False

if len(somelist)==0:
    print True
else:
    print False

"""列表推导式"""
list = [x +'a' for x in somelist]
print list

list = [x +'a' for x in somelist if x == 'c']
print list