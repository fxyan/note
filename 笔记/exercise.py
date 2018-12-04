# 快速排序
def quick_sort(array):
    if len(array) < 2:
        return array
    else:
        index = array[0]
        left_list = [x for x in array[1:] if x <= index]
        right_list = [x for x in array[1:] if x > index]
        return quick_sort(left_list) + [index] + quick_sort(right_list)


# 冒泡排序
def bubble_sort(array):
    l = len(array)
    for i in range(l-1):
        for j in range(l-1-i):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    return array


# 插入排序
def insert_sort(array):
    l = len(array)
    for i in range(1, l):
        index = i
        value = array[i]
        while index > 0 and value < array[index-1]:
            array[index] = array[index-1]
            index -= 1
        array[index] = value
    return array


# 归并排序
def marge_sort(array):
    if len(array) <= 1:
        return array
    else:
        mid = int(len(array) / 2)
        left_list = array[:mid]
        right_list = array[mid:]
        new_list = new_marge_sort(left_list, right_list)
        return new_list


def new_marge_sort(left_list, right_list):
    left = right = 0
    len_left = len(left_list)
    len_right = len(right_list)
    new_list = []
    while left < len_left and right < len_right:
        if left_list[left] < right_list[right]:
            new_list.append(left_list[left])
            left += 1
        else:
            new_list.append(right_list)
            right += 1
    while left < len_left:
        new_list.append(left_list[left])
        left += 1
    while right < len_right:
        new_list.append(right_list[right])
        right += 1
    return new_list


# 选择排序
def select_sort(array):
    l = len(array)
    for i in range(l-1):
        index = i
        for j in range(i+1, l):
            if array[index] > array[j]:
                index = j
        if index != i:
            array[i], array[index] = array[index], array[i]
    return array


def test():
    ll = LinkList()
    print(ll.tailnode)
    ll.append(33)
    ll.append(343)
    ll.append(334)
    ll.append(3267)
    print(list(ll))
    print(ll.find(334))
    print(ll.tailnode.value)
    print(ll.remove(3267))
    print(ll.tailnode.value)
    print(list(ll))
    print(ll.insert(334, 233))
    print(list(ll))


class pow():
    def __init__(self, n):
        self.n = n
        self.x = 0

    def __iter__(self):
        return self

    def __next__(self):
        x = self.x
        if self.x < self.n:
            self.x += 1
            return x
        else:
            raise StopIteration


# if __name__ == '__main__':
#     xx = [2, 4, 1, 3, 7, 4, 7, 2, 0]
#     for i in pow(10):
#         print(i)
#     # print(quick_sort(xx))
#     # print(bubble_sort(xx))
#     # print(select_sort(xx))
#     # print(insert_sort(xx))
#     # print(marge_sort(xx))
#     # import uuid
#     # names = [
#     #     'liu',
#     #     'trtre',
#     #     'name',
#     #     'web',
#     #     'python',
#     # ]
#     # ht = hashmap()
#     # for key in names:
#     #     value = uuid.uuid4()
#     #     # print(value)
#     #     ht.add(key, value)
#     #     print('add 元素', key, value)
#     # for key in names:
#     #     v = ht.get(key)
#     #     print('get 元素', key, v)
#     # ht.items()
#     # for i in ht.values():
#     #     # print(i)
#     # ht['wang'] = 23333
#     # print(ht['wang'])
#     # v = ht.get('wang')
#     # print('get 元素', 'wang', v)
class HashTable(object):
    def __init__(self):
        self.table_size = 20007
        self.table = [0] * self.table_size

    def add(self, key, value):
        index = self._index(key)
        pass

    def
