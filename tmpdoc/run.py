# -*- coding: utf-8 -*-

"""
Usage: ves run [OPTIONS] SCRIPT

Options:
    --help  Show this message and exit.
"""

# import os
# import click

# test = 1


# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)

# if __name__ == '__main__':
#     hello()
# print os.path

# @click.command(
#     context_settings={
#         "ignore_unknown_options": True,
#         "allow_extra_args": True
#     },
#     add_help_option=False)
# # @click.argument('script_or_uri', required=True)
# # @click.pass_context
# def run(ctx, script_or_uri):
#     group_name = ctx.parent.command.name + ' ' if ctx.parent else ''
#     prog_name = "{}{}".format(group_name, ctx.command.name)

#     import sys
#     sys.argv = [prog_name] + ctx.args

#     try:
#         pass
#         # module, func = script_or_uri.rsplit(':', 1)
#         # m = __import__(module, globals(), locals(), [func], 0)
#         # return getattr(m, func)()
#     except ValueError:
#         script = script_or_uri
#         return execfile(script, {'__name__': '__main__', '__file__':
#                                  os.path.realpath(script)})


# if __name__ == '__main__':
#     # pylint: disable=E1120
#     run()


# class C(object):
#     def __init__(self, x):
#         self.x = x

#     def getx(self):
#         print 'get x from c'
#         return self.x

#     # 添加一个属性'y'
#     y = property(getx)


# c = C(1)

# print c.y
# P   A   H   N
# A P L S I I G
# Y   I   R

# Definition for singly-linked list.
# def findrepeateddnasequences(s):
#     print s
#     s_len = len(s) - 10
#     if s_len < 0:
#         return []
#     data = dict()
#     rdata = set()
#     i = 0
#     while i <= s_len:
#         item = s[i:10 + i]
#         if not data.has_key(item):
#             data.update({item: 1})
#         else:
#             rdata.add(item)
#         i += 1
#     return list(rdata)
# s = "AAAAAAAAAAA"
# print findrepeateddnasequences(s)
def bubble(nums, asc=True):
    '''
        冒泡排序：相邻的数据相比较交换位置，把大的数据
    '''
    nums_size = len(nums)
    swapped = True
    while swapped:
        swapped = False
        for i in xrange(nums_size):
            for j in xrange(1, nums_size - i):
                if nums[j] < nums[j - 1]:
                    nums[j - 1], nums[j] = nums[j], nums[j - 1]
                    swapped = True
    return nums


def select(nums):
    """
        选择排序的特点就是依次把最小的，次小的排到最前面, 和冒泡立刻交换数据不同的是
        选择排序会使用一个哨兵监控最小的值
    """
    nums_size = len(nums)
    for i in xrange(nums_size):
        # 选择一个最小的哨兵
        guard_key = i
        for j in xrange(i, nums_size):
            if nums[j] < nums[guard_key]:
                guard_key = j
        # 赋值nums[i] 为最小值
        nums[i], nums[guard_key] = nums[guard_key], nums[i]

    return nums


def insert(nums):
    """
        插入排序：nums[0....i....j...n] 其中nums[0...i]是有序的，把nums[j...n]插入
        到nums[0....i]中
    """
    nums_size = len(nums)
    for i in xrange(nums_size):
        j = i + 1
        # 超出边界
        if j >= nums_size:
            break
        # 等待被插入的数据
        guard = nums[j]
        # 在i之前的数据都是有序的
        while i >= 0:
            # 哨兵数据如果小于nums[i]， 则需要顺延已经排好的数据
            if nums[i] > guard:
                nums[i + 1] = nums[i]
                # 空出来的位置用哨兵补上去
                nums[i] = guard
            i -= 1
    return nums


def merge(nums):
    """
        归并排序的思想：把一个list拆成左右两个list，分别对这两个list排序之后，再把两个list
        重新排列，从而得到一个排序好的list，
    """
    def do_merge(left, right):
        i, j = 0, 0
        # result类型是list, 可变类型，虽然result是局部变量，但不会因此而销毁
        result = []
        while i < len(left) and j < len(right):
            print left[i], right[j]
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # left=[1, 5] right[3, 6]经过以上的逻辑sorted_list = [1, 3, 5]
        # 现在还需要把没有加入或result里面
        if left[i:]:
            result += left[i:]
        if right[j:]:
            result += right[j:]

        return result

    # 现在要做的事情就是把nums拆成多个子nums，但len(nums) <= 1，说明递归到了最深一层，跳出递归
    # 使用递归的时候，一定要想清楚跳出递归的条件
    if len(nums) <= 1:
        return nums
    middle = len(nums) / 2
    # 递归后一个结果是前一个递归的输入值
    left = merge(nums[middle:])
    right = merge(nums[:middle])

    return do_merge(left, right)


def quick(nums, low, high):
    """
        快速排序的思想：分而治之，找出一个基准数值pivot, 保证 i<pivot<j同时
        nums[0...] < nums[pivot] < nums[j.....n]

        找到了pivot之后，就把nums分成了两部分nums[0....pivot + 1], nums[pivot-1....n]
        分别对这两部分递归排序即可
    """
    if not nums or low >= high:
        return nums

    def partition(nums, low, high):
        """
        nums = [4, 2, 5, 6, 1] povit = 4, low = 0, high = 4

        high向左遍历，直到a[high] < povit, 遇到1，此时low = 0, high = 4
        把这个移动到povit的左边 a[low] = a[high]
        此时low=1 nums=[1, 2, 5, 6, 1] povit=4, high=4

        low向右遍历，直到a[low] > povit, 遇到5, 此时low=2, 此时应该这个大于povit移动到右边
        a[high] = a[low] = 5， 移动之后，nums=[1, 2, 5, 6, 5]

        然后把low赋值 nums[low] = pivot 这样之后nums[1,2, 4, 6, 5] 这样pos这就是low的值

        i = 1, j = 3, 此时povit = a[1] = 2
        """
        # 把第一个数当作povit
        pivot = nums[low]
        while low < high:
            while low < high and nums[high] > pivot:
                high -= 1
            nums[low] = nums[high]

            while low < high and nums[low] < pivot:
                low += 1
            nums[high] = nums[low]
        # [3, 4, 5, 2]
        nums[low] = pivot
        return low

    if low < high:
        positon = partition(nums, low, high)
        quick(nums, 0, positon - 1)
        quick(nums, positon + 1, high)
    return nums


# print quick([3, 4, 11, 2], 0, 3)
#

# class Tobj(object):

#     x = 100

#     @property
#     def x(self):
#         print 'do property'
#         return 1000

# context = Tobj()


# def a(context):
#     print context.x
#     print 'a method execute:', id(context)


# def b(context):
#     print context.x
#     print 'b method execute:', id(context)


# a(context)
# b(context)

# print context
# print id(context)


class A(dict):

    def __getitem__(self, name):
        return self[name]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, attr, value):
        print 'set by __getattr__ method attr is {}, value is {}'.format(attr, value)
        super(A, self).__setattr__(attr, value)
a = A()
a.b = 2
print a['b']
