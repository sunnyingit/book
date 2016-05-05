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
def longestincreasingpath(nums):
    vertical = len(nums)
    y = vertical
    item = dict()
    for num in nums:
        length = len(num)
        for k, v in enumerate(num):
            item["val"] = num[k]
            if k - 1 > 0 and num[k] > num[k + 1]:


            if k + 1 < length:
            if y + 1 < vertical:
            if y - 1 > 0:
            items.append(item)
        y -= 1
    return items

print longestincreasingpath([[1, 2, 3]])
