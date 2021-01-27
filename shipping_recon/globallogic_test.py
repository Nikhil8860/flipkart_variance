# {3: ['abc', 'cab'], 4: ['abcd', 'dcba'], 5: ['abcde']}
#     dct_list = ['abc', 'cab', 'abcd', 'dcba', 'abcde']


"""
    dct = dict(a='20000', d='10', b='300', c='5000')
 Value {'d': '10', 'b': '300', 'c': '5000', 'a': '20000',}
"""


def make_count_dict(dct_list):
    d = {}
    for i in dct_list:
        d.setdefault(len(i), []).append(i)
    print(d)


"""
    dct = dict(a='20000', d='10', b='300', c='5000')
 Value {'d': '10', 'b': '300', 'c': '5000', 'a': '20000',}
"""
dct = dict(a='20000', d='10', b='300', c='5000')

d = {}
for v in sorted(dct, key=lambda v: len(dct[v])):
    d[v] = dct[v]
print(d)

"""
select * from emp where joining_date IN 
(select DISTINCT top 5 date from employee CONVERT(date, ) DESC)
"""

"""
find no. of employee table salary > avg

"""

"""select salary from Salary_table
    where salary > (select AVG(salary) from salary_table))  
"""
a = frozenset({1, 2, 3, 4, 5})


def sockMerchant(n, ar):
    count = 0
    for i in set(ar):
        v = ar.count(i)
        if v // 2 != 0:
            count += v // 2
    print(count)


def countingValleys(steps, path):
    a = path[0]
    for i in range(1, len(path) - 1):
        if path[i] != a and path[i + 1] == a:
            print(path[i])


def jumpingOnClouds(c):
    if len(c) == 1:
        return 0
    if len(c) == 2:
        return 0 if c[1] == 1 else 1
    if c[2] == 1:
        return 1 + jumpingOnClouds(c[1:])
    if c[2] == 0:
        return 1 + jumpingOnClouds(c[2:])


if __name__ == '__main__':
    arr = [0, 0, 1, 0, 0, 1, 0]
    print(jumpingOnClouds(arr))
