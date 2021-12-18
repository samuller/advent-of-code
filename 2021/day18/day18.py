#!/usr/bin/env python3
import fileinput
from collections import deque


# A tree where a list of leafs can be constructed
class Tree:
    def __init__(self, parent, data=None):
        self.parent = parent
        self.left = None
        self.right = None
        self.data = data

    def __str__(self):
        if self.data is None:
            return f"[{self.left},{self.right}]"
        else:
            assert self.left is None
            assert self.right is None
            return f"{self.data}"

    def to_list(self):
        return eval(str(self))

    def is_leaf(self):
        if self.data is not None:
            assert self.left is None
            assert self.right is None
            return True
        return False

    def leaves(self):
        values = []
        Q = deque([self])
        while Q:
            curr = Q.pop()
            if curr.data is not None:
                values.append(curr)
            else:
                Q.append(curr.right)
                Q.append(curr.left)
        return values

    def leaf_data(self):
        values = []
        Q = deque([self])
        while Q:
            curr = Q.pop()
            if curr.data is not None:
                values.append(curr.data)
            else:
                Q.append(curr.right)
                Q.append(curr.left)
        return values

    def get_root(self):
        if self.parent is None:
            return self
        return self.parent.get_root()

    def next_left(self):
        if not self.is_leaf():
            assert False
        root = self.get_root()
        leaves = root.leaves()
        for idx in range(1, len(leaves)):
            leaf = leaves[idx]
            if leaf is self:
                return leaves[idx-1]
        return None

    def next_right(self):
        if not self.is_leaf():
            assert False
        root = self.get_root()
        leaves = root.leaves()
        for idx in range(len(leaves)-1):
            leaf = leaves[idx]
            if leaf is self:
                return leaves[idx+1]
        return None
    
    def expand(self):
        # print("expand")
        pair = self.to_list()
        next_left = self.left.next_left()
        if next_left is not None:
            # print("left", next_left)
            next_left.data += pair[0]
        next_right = self.right.next_right()
        if next_right is not None:
            # print("right", next_right)
            next_right.data += pair[1]

    def explode(self, start_depth=1):
        if self.data is not None:
            return self.data, False
        # print(start_depth, self)
        did_it = False
        if start_depth == 4:
            if not self.left.is_leaf():
                self.left.expand()
                # self.right.data += pair[1] # lipairty[0]
                self.left = Tree(self, 0)
                did_it = True
            if not self.right.is_leaf():
                # pair = self.right.to_list()
                self.right.expand()
                # self.left.data += pair[0] # pair[1]
                self.right = Tree(self, 0)
                did_it = True
        else:
            if not self.left.is_leaf():
                self.left, did_it = self.left.explode(start_depth+1)
            if not self.right.is_leaf() and not did_it:
                self.right, did_it = self.right.explode(start_depth+1)
        return self, did_it

    def magnitude(self):
        if self.is_leaf():
            return self.data
        return 3*self.left.magnitude() + 2*self.right.magnitude()


def parse_to_tree(pairs, parent=None):
    assert len(pairs) == 2
    left, right = pairs
    root = Tree(parent, None)
    if isinstance(left, list):
        root.left = parse_to_tree(left, root)
    else:
        root.left = Tree(root, left)
    if isinstance(right, list):
        root.right = parse_to_tree(right, root)
    else:
        root.right = Tree(root, right)
    return root


def test_explode(listy):
    return str(parse_to_tree(listy).explode()[0])


# 9:30 - complete asserts
assert test_explode([[[[[9,8],1],2],3],4]) == "[[[[0,9],2],3],4]", test_explode([[[[[9,8],1],2],3],4])[0]
assert test_explode([7,[6,[5,[4,[3,2]]]]]) == "[7,[6,[5,[7,0]]]]"
assert test_explode([[6,[5,[4,[3,2]]]],1]) == "[[6,[5,[7,0]]],3]", test_explode([[6,[5,[4,[3,2]]]],1])
assert test_explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", test_explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
assert test_explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]", test_explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])


def split(num):
    assert isinstance(num, int)
    down = num // 2
    up = (num // 2) + (num % 2)
    return [down, up]


assert split(10) == [5,5]
assert split(11) == [5,6]
assert split(12) == [6,6]


def split_leaf(leaf):
    assert leaf.is_leaf()
    pair = split(leaf.data)
    leaf.data = None
    leaf.left = Tree(leaf, pair[0])
    leaf.right = Tree(leaf, pair[1])
    assert not leaf.is_leaf()
    return leaf


assert str(split_leaf(Tree(None, 10))) == "[5,5]"
assert str(split_leaf(Tree(None, 11))) == "[5,6]"
assert str(split_leaf(Tree(None, 12))) == "[6,6]"


def split_tree(tree):
    leaves = tree.leaves()
    for leaf in leaves:
        if leaf.data >= 10:
            leaf = split_leaf(leaf)
            return True
    return False


def reduce(left, right):
    combined = Tree(None, None)
    combined.left = left
    left.parent = combined
    combined.right = right
    right.parent = combined
    # addition
    while True:
        # explodes: nested 4 times
        combined, did_explode = combined.explode()
        if did_explode:
            continue
        # splits: x >= 10
        did_split = split_tree(combined)
        if did_split:
            continue
        break
    return combined


def test_reduce(list1, list2):
    return str(reduce(parse_to_tree(list1), parse_to_tree(list2)))


assert test_reduce([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", test_reduce([[[[4,3],4],4],[7,[[8,4],9]]], [1,1])


def test_mag(listy):
    return parse_to_tree(listy).magnitude()


assert test_mag([[1,2],[[3,4],5]]) == 143
assert test_mag([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384
assert test_mag([[[[1,1],[2,2]],[3,3]],[4,4]]) == 445
assert test_mag([[[[3,0],[5,3]],[4,4]],[5,5]]) == 791
assert test_mag([[[[5,0],[7,4]],[5,5]],[6,6]]) == 1137
assert test_mag([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488


# 4902 @ 10:20 - too high
def main():
    lists = [eval(line.strip()) for line in fileinput.input()]
    
    # Part 1
    summ = parse_to_tree(lists[0])
    for listy in lists[1:]:
        nxt = parse_to_tree(listy)
        summ = reduce(summ, nxt)
        # print(listy)
        # print(tree)
        # print(tree.leaf_data())
    # 10:08
    print(summ.magnitude())

    # Part 2
    max_mag = 0
    max_combo = None
    for idx_i, list_i in enumerate(lists):
        for idx_j, list_j in enumerate(lists):
            if idx_i == idx_j:
                continue
            tree_i = parse_to_tree(list_i)
            tree_j = parse_to_tree(list_j)
            mag = reduce(tree_i, tree_j).magnitude()
            if mag > max_mag:
                max_mag = mag
                max_combo = [idx_i, idx_j]

            # Have to recreate since they were altered by reduce()
            tree_i = parse_to_tree(list_i)
            tree_j = parse_to_tree(list_j)
            mag = reduce(tree_j, tree_i).magnitude()
            if mag > max_mag:
                max_mag = mag
                max_combo = [idx_j, idx_i]
    print(max_mag)
    print(max_combo)


if __name__ == '__main__':
    main()
