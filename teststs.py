"""
A>B>C>D>E>F>None
A>C>E>B>D>F>None
"""

head = None


class LinkedList:
    def __init__(self, data):
        self.data = data
        self.next = None


def find_odd_even():
    """A>B>C>D>E>F>None"""
    global head
    last = head
    p = None
    c = head

    while last.next:
        last = last.next

    new_last = last

    while c.data % 2 != 0 and c != last:
        new_last.next = c
        c = c.next
        new_last.next.next = None

    if c.data % 2 == 0:
        head = c

        while c != last:

            if c.data % 2 == 0:
                p = c
                c = c.next

            else:
                p.next = c.next
                c.next = None

                new_last.next = c
                new_last = c

                c = p.next
    else:
        p = c

    if new_last != last and last.data % 2 != 0:
        p.next = last.next
        last.next = None
        new_last.next = last


def add_val(val):
    global head
    node = LinkedList(val)
    node.next = head
    head = node


def print_data():
    global head
    t = head
    while t:
        print(t.data, end=" ")
        t = t.next
    print(" ")


if __name__ == '__main__':
    add_val(1)
    add_val(2)
    add_val(3)
    add_val(4)
    add_val(5)
    add_val(6)
    add_val(7)
    add_val(8)
    add_val(9)
    # LinkedList('b')
    # LinkedList('c')
    # LinkedList('d')
    print(head.data)
    print_data()
    find_odd_even()
    print(head.data)
    print_data()
