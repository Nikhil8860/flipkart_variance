x = [1, 2, 3, 4, 5]


def get():
    for i in x:
        yield i


a = get()
print(type(a))

print(list(a)[-1])
