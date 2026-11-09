class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        tail = None
        for value in values:
            node = Node(value)
            if tail is None:
                self.head = node
            else:
                tail.next = node
            tail = node

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def reverse(self):
        previous = None
        current = self.head
        while current is not None:
            following = current.next
            current.next = previous
            previous = current
            current = following
        self.head = previous

    def sort(self):
        self.head = _merge_sort(self.head)


def _merge_nodes(left, right):
    head = tail = None
    while left is not None and right is not None:
        if left.data <= right.data:
            node = left
            left = left.next
        else:
            node = right
            right = right.next

        if tail is None:
            head = node
        else:
            tail.next = node
        tail = node

    if tail is None:
        return left if left is not None else right
    tail.next = left if left is not None else right
    return head


def _merge_sort(head):
    if head is None or head.next is None:
        return head

    slow = head
    fast = head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    right = slow.next
    slow.next = None
    return _merge_nodes(_merge_sort(head), _merge_sort(right))


def merge_sorted_lists(left, right):
    if left is right:
        raise ValueError("Не можна об'єднати список із самим собою")

    merged = LinkedList()
    merged.head = _merge_nodes(left.head, right.head)
    left.head = None
    right.head = None
    return merged


if __name__ == "__main__":
    numbers = LinkedList([4, 2, 5, 1, 3])
    numbers.reverse()
    print("Реверс:", list(numbers))
    numbers.sort()
    print("Сортування:", list(numbers))

    first = LinkedList([1, 3, 5])
    second = LinkedList([2, 4, 6])
    print("Злиття:", list(merge_sorted_lists(first, second)))
