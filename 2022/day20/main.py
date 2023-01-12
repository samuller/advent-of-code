#!/usr/bin/env python3
import fileinput

import sys; sys.path.append("../..")
from lib import *


def sgn(val):
    if val < 0:
        return -1
    elif val > 0:
        return 1
    else:
        return 0


def construct(order, nums):
    new_list = []
    for new_idx in range(len(order)):
        old_idx = order[new_idx]
        new_list.append(nums[old_idx])
    return new_list


def mix(nums, new_to_old=None):
    debug = True
    size = len(nums)

    # #1
    # new_order = nums.copy()
    # new_order[idx] = new_idx + 1
    # for key in new_order:
    #     if new_order[key] >= new_idx:
    #         new_order[key] += 1

    # #5 8:35-8:40 keeping track of curr_idx...
    # new_list = nums.copy()
    # curr_idx = {old: old for old in range(size)}
    # for old_idx in range(size):
    #     value = nums[old_idx]
    #     new_idx = (old_idx + num) % size
    #     if new_idx > old_idx:
    #         new_list.insert(new_idx + 1, value)
    #         new_list = [n for i, n in enumerate(new_list) if i != old_idx]
    #     elif new_idx < old_idx:
    #         new_list.insert(new_idx + 1, value)
    #         new_list = [n for i, n in enumerate(new_list) if i != old_idx]

    if new_to_old is None:
        # key-to-value
        new_to_old = {old: old for old in range(size)}
        # old_to_new = {old: old for old in range(size)}
    for old_idx in range(size):
        print(old_idx)
        num = nums[old_idx]
        curr_idx = (list(new_to_old.keys())[list(new_to_old.values()).index(old_idx)])
        print("{" + f"{num}" + "}" + f" ({curr_idx})") if debug else None
        # curr_idx = new_to_old[old_idx]

        # new_idx = (idx + num) % size
        # print(f"{num} -> [{new_idx}]")

        if num > 0:
            shift = +1
        elif num < 0:
            shift = -1
        else:
            continue

        # #2 - swap each in-turn
        # #4 - plus, crossing boundaries renumbers everything
        # works for part 1!
        super_shift = 0
        # for cnt in range(abs(num)):
        #     curr = (curr_idx + shift*cnt) % size
        #     nxt = (curr_idx + shift*(cnt + 1)) # % size
        #     # If we cross (actually touch) the list end/start boundary
        #     if nxt == size-1:  # >=
        #         print(f"++++++1 {nxt}") if debug else None
        #         super_shift = +1
        #     elif nxt == 0:  # <=
        #         print(f"------1 {nxt}") if debug else None
        #         super_shift = -1
        #     nxt = nxt % size
        #     assert nxt == (curr + shift*1) % size
        #     print(f"{curr} <-> {nxt}") if debug else None
        #     # If we cross back over our old location
        #     if nxt == curr_idx:
        #         super_shift = 0
        #     # Swap values
        #     new_to_old[curr], new_to_old[nxt] = new_to_old[nxt], new_to_old[curr]
        #     print(new_to_old) if debug else None
        #     # print("  ", old_to_new)
        #
        # if super_shift == -1:
        #     # start gets appended to end, and all values move 1 down
        #     start = new_to_old[0]
        #     for i in range(1, size):
        #         new_to_old[i - 1] = new_to_old[i]
        #     new_to_old[size-1] = start
        #     print("shift -1") if debug else None
        # if super_shift == +1:
        #     # # end gets pre-pended to start, and all values move 1 up 
        #     end = new_to_old[size-1]
        #     for i in range(size - 2, -1, -1):  #(0, size - 1):
        #         new_to_old[i + 1] = new_to_old[i]
        #     new_to_old[0] = end
        #     print("shift +1") if debug else None

        # 09:05 #6 = #3 for part 2
        new_idx = curr_idx + num
        while new_idx > size:
            super_shift = +1
            new_idx -= size
            if new_idx >= curr_idx:
                super_shift = 0
        while new_idx < 0:
            super_shift = -1
            new_idx += size
            if new_idx <= curr_idx:
                super_shift = 0
        if num < 0:
            new_idx = max(0, new_idx - 1)
        print(f"{curr_idx} <-> {new_idx}") if debug else None
        # Do extraction
        print(f"extr: {curr_idx + 1} {size}")
        for after_idx in range(curr_idx + 1, size):
            new_to_old[after_idx - 1] = new_to_old[after_idx]
        # Do insertion
        print(f"ins: {size} {new_idx}")
        for after_idx in range(size - 2, new_idx - 1, -1):  #(new_idx, size - 1):
            new_to_old[after_idx + 1] = new_to_old[after_idx]
        new_to_old[new_idx] = old_idx

        # # Do extraction and insertion
        # if curr_idx < new_idx < size:
        #     for btw_idx in range(curr_idx + 1, new_idx + 1):
        #         new_to_old[btw_idx - 1] = new_to_old[btw_idx]
        # if 0 < new_idx < curr_idx:
        #     pass
        # if curr_idx < new_idx < size:
        #     pass
        # new_to_old[new_idx] = curr_idx

        # Not a swap!
        # new_to_old[curr_idx], new_to_old[new_idx] = new_to_old[new_idx], new_to_old[curr_idx]

        print(new_to_old) if debug else None
        # print("  ", old_to_new)

        # #3 - swap only start/end positions?
        # new_idx = (curr_idx + num) % size
        # print(f"{curr_idx} <-> {new_idx}")
        # new_to_old[curr_idx], new_to_old[new_idx] = new_to_old[new_idx], new_to_old[curr_idx]
        # print(new_to_old)

        print("Cons:", construct(new_to_old, nums)) if debug else None
        assert len(new_to_old.values()) == len(set(new_to_old.values()))
        assert sorted(list(new_to_old.keys())) == sorted(list(new_to_old.values()))
        assert sorted(list(new_to_old.keys())) == list(range(size))
    # print(construct(new_to_old, nums))
    # return construct(new_to_old, nums)
    return new_to_old


class Node:
   def __init__(self, dataval=None):
      self.dataval = dataval
      self.nextnode: Node = None

class SLinkedList:
    def __init__(self):
        self.headnode: Node = None

    def to_list(self):
        new_list = []
        curr = self.headnode
        while curr.nextnode is not None:
            new_list.append(curr.dataval)
            curr = curr.nextnode
        new_list.append(curr.dataval)
        return new_list

    def get_idx(self, node_val):
        idx = 0
        curr = self.headnode
        while curr.nextnode is not None:
            if curr.dataval == node_val:
                return idx
            curr = curr.nextnode
            idx += 1
            if curr == self.headnode:
                raise RecursionError("Infinite loop in linked list")
        if curr.dataval == node_val:
            return idx
        return None

    def tails(self):
        curr = self.headnode
        prev = None
        while curr.nextnode is not None:
            prev = curr
            curr = curr.nextnode            
        return prev, curr

    def remove(self, idx: int):
        if idx == 0:
            pre_tail, tail = self.tails()
            tail.nextnode = self.headnode.nextnode
            pre_tail.nextnode = None
            return self.headnode
        curr_idx = 0
        curr = self.headnode
        prev = None
        while curr.nextnode is not None:
            if curr_idx == idx:
                prev.nextnode = curr.nextnode
                curr.nextnode = None
                return curr
            curr = curr.nextnode
            curr_idx += 1
        return None

    def insert_after(self, idx, new_node):
        if idx == -1:
            new_node.nextnode = self.headnode
            self.headnode = new_node
            return True
        curr_idx = 0
        curr = self.headnode
        while curr.nextnode is not None:
            if curr_idx == idx:
                new_node.nextnode = curr.nextnode
                curr.nextnode = new_node
                return True
            curr = curr.nextnode
            curr_idx += 1
        return False

    def move(self, old_idx, new_idx):
        if old_idx == new_idx:
            return True
        node = self.remove(old_idx)
        if old_idx < new_idx:
            return self.insert_after(new_idx-2, node)
        else:
            return self.insert_after(new_idx-1, node)


def ll_mix(nums, new_to_old=None):
    size = len(nums)
    debug = True

    llist = SLinkedList()
    for idx, num in enumerate(nums):
        node = Node((idx, num))
        if llist.headnode is None:
            llist.headnode = node
        else:
            # Add at end
            curr = llist.headnode
            while curr.nextnode is not None:
                curr = curr.nextnode
            curr.nextnode = node

    for old_idx in range(size):
        num = nums[old_idx]
        print(old_idx, num)
        curr_idx = llist.get_idx((old_idx, num))
        new_idx = (curr_idx + num) % size
        print("{" + f"{num}" + "}" + f" ({curr_idx} -> {new_idx})") if debug else None
        print([n for _, n in llist.to_list()])
        success = llist.move(curr_idx, new_idx)
        assert success
    print(llist.to_list())

    new_to_old = {old: old for old in range(size)}


# 9:40 - should've used a double linked list where each node stores the value and old index
# 9:51 - stop
def main():
    nums = [int(line.replace("\n", "")) for line in fileinput.input()]
    debug = False

    print(nums) if debug else None
    print(len(nums), len(set(nums)))

    mix_times = 1

    # 9:55 - 10:33
    ll_mix(nums)
    exit()

    # Part 2
    # nums = [n*811589153 for n in nums]
    # mix_times = 10

    new_to_old = None
    for _ in range(mix_times):
        new_to_old = mix(nums, new_to_old)
    decrypted = construct(new_to_old, nums)

    start_idx = decrypted.index(0)
    print(
        decrypted[(start_idx+1000) % len(nums)] \
        + decrypted[(start_idx+2000) % len(nums)] \
        + decrypted[(start_idx+3000) % len(nums)]
    )


if __name__ == '__main__':
    main()

# Initial arrangement:
# 1, 2, -3, 3, -2, 0, 4

# 1 moves between 2 and -3:
# 2, 1, -3, 3, -2, 0, 4

# 2 moves between -3 and 3:
# 1, -3, 2, 3, -2, 0, 4

# -3 moves between -2 and 0:
# 1, 2, 3, -2, -3, 0, 4

# 3 moves between 0 and 4:
# 1, 2, -2, -3, 0, 3, 4

# -2 moves between 4 and 1:
# 1, 2, -3, 0, 3, 4, -2

# 0 does not move:
# 1, 2, -3, 0, 3, 4, -2

# 4 moves between -3 and 0:
# 1, 2, -3, 4, 0, 3, -2