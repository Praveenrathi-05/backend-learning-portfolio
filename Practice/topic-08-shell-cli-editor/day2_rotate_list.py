"""
Topic 8, Day 2 DSA Micro-Drill: rotate_list(lst, k)

Rotate a list right by k positions.

Example:
    rotate_list([1, 2, 3, 4, 5], 2) -> [4, 5, 1, 2, 3]

Core idea: split the list into two pieces at a cut point -- the last k
elements, and everything before them -- then swap their order (last piece
first, then first piece) using slicing and + concatenation.

Two edge cases discovered and handled while testing:
1. k larger than the list length -- fixed with k % len(nums), so k "wraps
   around" to an equivalent smaller rotation amount.
2. An empty list -- len([]) is 0, and k % 0 raises ZeroDivisionError.
   Guarded with an early return before the modulo ever runs.
"""


def rotate_list(nums, k):
    if len(nums) == 0:
        return nums
    num_length = len(nums)
    cut = num_length - k % num_length
    return nums[cut:] + nums[:cut]


if __name__ == "__main__":
    print(rotate_list([1, 2, 3, 4, 5], 2))    # [4, 5, 1, 2, 3]
    print(rotate_list([1, 2, 3, 4, 5], 12))   # [4, 5, 1, 2, 3] -- k wraps via modulo
    print(rotate_list([], 3))                  # []              -- empty list guard
