# -*- coding: UTF-8 -*-
# N阶楼梯，可以选择一次爬1阶，也可以一次爬2阶，有多少种爬法
# 思路: 当只有1阶， 那只有1种方法
#      当有2阶，2种方法，可以一次爬1阶，还可以一次爬2阶，2种方法
#      当楼梯的数量大于2时，无外乎就是两种选择，一次迈1步，或者一次迈2步
#      选择第一种走法，先迈1步，那走完剩下的楼梯就是f(n-1)种走法，
#      选择第二种走法，先迈2步，那走完剩下的楼梯就是f(n-2)种走法
#      把这两种选择加起来的走法就是走楼梯可能的走法 = f(n-1) + f(n-2)
#      f(n) = f(n-1) + f(n-2)
#      f(3) = f(2) + f(1)
#      f(4) = f(3) + f(2) = f(2) + f(1) + f(2)
#      如果还可以一次迈3步，那走完剩下的就是f(n-3)走法
#      f(n) = f(n-1) + f(n-2) + f(n-3)
#
#


def recursion(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n > 2:
        return recursion(n - 1) + recursion(n - 2)


# 既然 f(n) = f(n-1) + f(n-2)
# f[2] = f[1] + f[0]
# f[3] = f[2] + f[1]
# f[4] = f[3] + f[2]
# f[4] = (f[2] + f[1])  + (f[1] + f[0]) = (f[1] + f[0] + f[1]) + + (f[1] +
# f[0])
def recursion_v1(n):
    step = [1, 1, 0]
    if n == 1:
        return 1
    i = 2
    while i <= n:
        step[2] = step[0] + step[1]
        step[0] = step[1]
        step[1] = step[2]
        i += 1
    return step[2]


# 可以一次爬三步

def recursion_v2(n):
    if n == 1:
        return 1

    if n == 2:
        return 2
    if n == 3:
        return 4
    if n > 3:
        return recursion_v2(n - 1) + recursion_v2(n - 2) + recursion_v2(n - 3)


# 既然 f(n) = f(n-1) + f(n-2) + f(n-3)
# 如果看成一个数组，那么就是a[n] = a[n-1] + a[n-2] + a[n-3]
# a[4] = a[3] + a[2] + a[1]
# a[5] = a[4] + a[3] + a[2]
# a[6] = a[5] + a[4] + a[3]
def recursion_v3(n):
    step = [0, 1, 1, 2, 0]
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4
    i = 4
    while (i <= n):
        step[4] = step[1] + step[2] + step[3]
        step[3] = step[1] + step[2] + step[3]
        i += 1
    return step[4]

# a = recursion_v2(10)
# print a

s = [0] * 104
s[0] = 1
# s[1] = s[0]
# s[2] = s[0] + s[1]
# s[3] = s[0] + s[1] + s[2]
# 循环1次s[1] = s[1] + s[0]   = 1
# 循环1次s[2] = s[2] + s[0]   = 1
# 循环1次s[3] = s[3] + s[0]   = 1
#
# 循环2次s[2] = s[2] + s[1]   = 2 s[2] + s[1] +s[0]
# 循环2次s[3] = s[3] + s[1]   = 2
# 循环2次s[4] = s[3] + s[1]   = 2
#
# 循环3次s[3] = s[3] + s[2]   = 4  = (s[3] + s[1]) + (s[2] + s[1])
# 循环3次s[4] = s[4] + s[2]   = 4
# 循环3次s[5] = s[5] + s[2]   = 2
#
# 循环4次s[4] = s[4] + s[3]   = (s[4] + s[2]) + s[3] + s[2]
# 循环4次s[5] = s[5] + s[3]   = 2
# 循环4次s[6] = s[6] + s[3]   = 2
for i in xrange(5):
    s[i + 1] = s[i + 1] + s[i]
    s[i + 2] = s[i + 2] + s[i]
    s[i + 3] = s[i + 3] + s[i]
print s[5]
