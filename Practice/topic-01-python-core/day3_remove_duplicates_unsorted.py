# Topic 1, Day 3 Extension
# remove_duplicates_inplace: works on UNSORTED lists too.
# Swaps "compare to previous element" for "have I seen this value anywhere before?"
# using a set -- same two-pointer overwrite/trim structure as the sorted version.


def remove_duplicates_inplace(lst):
    s = set()
    k = 0
    i = 0
    while i < len(lst):
        if lst[i] not in s:
            s.add(lst[i])
            lst[k] = lst[i]
            k += 1
        i += 1
    del lst[k:]


nums = [3, 1, 2, 1]
remove_duplicates_inplace(nums)
print(nums)  # [3, 1, 2]
