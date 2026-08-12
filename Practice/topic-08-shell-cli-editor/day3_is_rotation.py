"""
Topic 8, Day 3 DSA Micro-Drill: is_rotation(list1, list2)

Given two lists, determine whether list2 is a rotation of list1.

Example:
    is_rotation([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]) -> True   (this is the k=2 case)
    is_rotation([1, 2, 3], [1, 3, 2]) -> False              (same elements, wrong order)

Core idea: reuse rotate_list (from Day 2) instead of writing rotation
logic again. Try every rotation amount from 0 to len(l1)-1 -- that's the
full, minimal set of distinct rotations a list of length n can have.

Edge case handled: is_rotation([], []) -- range(len([])) is range(0), so
the loop body never runs at all. An explicit l1 == l2 check up front
catches this (and more generally, "no rotation needed" is itself a valid
rotation, by k=0 -- empty lists are just one example of that).
"""

from day2_rotate_list import rotate_list


def is_rotation(l1, l2):
    if l1 == l2:
        return True
    for i in range(len(l1)):
        if rotate_list(l1, i) == l2:
            return True
    return False


if __name__ == "__main__":
    print(is_rotation([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]))  # True
    print(is_rotation([1, 2, 3], [1, 3, 2]))                # False
    print(is_rotation([], []))                                # True -- empty list edge case
