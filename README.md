# 🚀 DSA in Java

📊 **[View Interactive Dashboard →](https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/)**

---

Automatically generated list of solved problems (grouped by topic).

| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |
|---|----------|-----------|--------|-----------------|----------|--------------|
| **Array (8)** |  |  |  |  |  |  |
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/description/.) | [Code](dsa/Array/TwoSum.java) | Easy | HashMap (Complement Pattern) | No | Use map to store num[i],index. |
| 2 | [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) | [Code](dsa/Array/Two Sum II.java) | Easy | Two Pointer | no | modified bimaey search(as it is sorted) |
| 3 | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | [Code](dsa/Array/trapping-rain-water.java) | Medium | two pointer(without space) | yes | store max left & right heigh for every index then caculate trap water |
| 4 | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Code](dsa/Array/container-with-most-water.java) | Easy | Two Pointer | no | Two pointer- calculate area whatever hight is slower from low & high move that |
| 5 | [26. Remove Duplicates frm sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description) | [Code](dsa/Array/Remove Duplicates from Sorted Array.java) | Easy | Two Pointer | no | two pointer if find different element then update element of slow |
| 6 | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/description/) | [Code](dsa/Array/Product_Except_Self.java) | Easy | prefix & sufix | No | prefix and suffix prodcut store in array and do product later |
| 7 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/description.) | [Code](dsa/Array/MoveZeros.java) | Easy | Two Pointer | Yes | Count zeros and if count>0 then swap number by that much index |
| 8 | [169. Majority Element](https://leetcode.com/problems/majority-element/description/) | [Code](dsa/Array/Majority Element.java) | Easy | Moore Voting Algorithm. | no | Moore Voting Algorithm. maintain frequency & max element |
|  |  |  |  |  |  |  |
| **LinkedList (3)** |  |  |  |  |  |  |
| 9 | [83. Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/) | [Code](dsa/LinkedList/remove-duplicates-from-sorted-list.java) | Easy | Two Pointer | no | two pointer= link the nodes if not match |
| 10 | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | [Code](dsa/LinkedList/reverse-linked-list.java) | Easy | Two Pointer | no | two point prev & curr swap one link at a time |
| 11 | [160. Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/) | [Code](dsa/LinkedList/intersection-of-two-linked-lists.java) | Easy | Two Pointer | no | As both length is diff if we start traversing another list then both will be at intersection |
|  |  |  |  |  |  |  |
| **recursion (3)** |  |  |  |  |  |  |
| 12 | [78. Subsets](https://leetcode.com/problems/subsets/description/) | [Code](dsa/recursion/find_Subsets.java) | Medium | backtracking | Yes | subsequence pattern to pick and not pick current element dual recursion call |
| 13 | [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | [Code](dsa/recursion/combination-sum-iI.java) | Hard | backtracking | Yes | - |
| 14 | [39. Combination Sum](https://leetcode.com/problems/combination-sum/description/) | [Code](dsa/recursion/combination-sum.java) | Medium | backtracking | Yes | same pattern pick not pick just we can pick same element mutiple time  so not inc that time Also handle other cases |
|  |  |  |  |  |  |  |
