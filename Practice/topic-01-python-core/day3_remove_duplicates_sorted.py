# Topic 1, Day 3 Homework
# remove_duplicates_inplace: mutate the original list (no new list returned)
# This version works correctly ONLY when the input is already sorted,
# since it only compares each element to the one immediately before it.


def remove_duplicates_inplace(lst):
    last_element = float("-inf")
    k = 0
    i = 0
    while i < len(lst):
        if last_element != lst[i]:
            lst[k] = lst[i]
            last_element = lst[i]
            k += 1
        i += 1
    del lst[k:]


nums = [1, 2, 2, 3, 3, 3]
remove_duplicates_inplace(nums)
print(nums)  # [1, 2, 3] -- original list mutated, no reassignment needed
