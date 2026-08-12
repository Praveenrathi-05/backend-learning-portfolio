"""
Topic 8, Day 1 DSA Micro-Drill: merge_sorted(list1, list2)

Merge two ALREADY-SORTED lists into one sorted list, without concatenating
and calling sorted() on the result.

Example:
    merge_sorted([1, 3, 5], [2, 4, 6]) -> [1, 2, 3, 4, 5, 6]
    merge_sorted([1, 2, 8], [1, 3, 4, 5, 9]) -> [1, 1, 2, 3, 4, 5, 8, 9]

Core idea: walk both lists at once with two index pointers (i, j), always
appending whichever front-most unused element is smaller. Once one list
runs out, the leftover of the other list is already sorted -- just extend
it onto the result directly, no more comparisons needed.

This is the exact building block behind merge sort.
"""


def merge_sorted(l1, l2):
    i = 0
    j = 0
    new_list = []
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            new_list.append(l1[i])
            i += 1
        else:
            new_list.append(l2[j])
            j += 1
    # Whichever list still has leftover elements is already sorted --
    # just tack the remainder on directly.
    new_list.extend(l1[i:])
    new_list.extend(l2[j:])
    return new_list


if __name__ == "__main__":
    print(merge_sorted([1, 3, 5], [2, 4, 6]))          # [1, 2, 3, 4, 5, 6]
    print(merge_sorted([1, 2, 8], [1, 3, 4, 5, 9]))     # [1, 1, 2, 3, 4, 5, 8, 9] -- tie + uneven lengths
