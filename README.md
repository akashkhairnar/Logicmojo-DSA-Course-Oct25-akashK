# 🚀 DSA in Java

📊 **[View Interactive Dashboard →](https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/)**

Automatically generated list of solved problems, grouped by topic.

### Array

| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |
|---|---------|---------|-------|---------|---------|-------------|
| 1 | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Code](dsa/Array/container-with-most-water.java) | Easy | Two Pointer | No | Two pointer- calculate area whatever hight is slower from low & high move that |
| 2 | [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) | [Code](dsa/Array/Two Sum II.java) | Easy | Two Pointer | No | modified bimaey search(as it is sorted) |
| 3 | [169. Majority Element](https://leetcode.com/problems/majority-element/description/) | [Code](dsa/Array/Majority Element.java) | Easy | Moore Voting Algorithm. | No | Moore Voting Algorithm. maintain frequency & max element |
| 4 | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/description/) | [Code](dsa/Array/Product_Except_Self.java) | Easy | prefix & sufix | No | prefix and suffix prodcut store in array and do product later |
| 5 | [26. Remove Duplicates frm sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description) | [Code](dsa/Array/Remove Duplicates from Sorted Array.java) | Easy | Two Pointer | No | two pointer if find different element then update element of slow |
| 6 | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | [Code](dsa/Array/trapping-rain-water.java) | Medium | two pointer(without space) | Yes | store max left & right heigh for every index then caculate trap water |
| 7 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/description.) | [Code](dsa/Array/MoveZeros.java) | Easy | Two Pointer | Yes | Count zeros and if count>0 then swap number by that much index |
| 8 | [Two Sum](https://leetcode.com/problems/two-sum/description/.) | [Code](dsa/Array/TwoSum.java) | Easy | HashMap (Complement Pattern) | No | Use map to store num[i],index. |

### LinkedList

| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |
|---|---------|---------|-------|---------|---------|-------------|
| 1 | [160. Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/) | [Code](dsa/LinkedList/intersection-of-two-linked-lists.java) | Easy | Two Pointer | No | As both length is diff if we start traversing another list then both will be at intersection |
| 2 | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | [Code](dsa/LinkedList/reverse-linked-list.java) | Easy | Two Pointer | No | two point prev & curr swap one link at a time |
| 3 | [83. Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/) | [Code](dsa/LinkedList/remove-duplicates-from-sorted-list.java) | Easy | Two Pointer | No | two pointer= link the nodes if not match |

### recursion

| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |
|---|---------|---------|-------|---------|---------|-------------|
| 1 | [39. Combination Sum](https://leetcode.com/problems/combination-sum/description/) | [Code](dsa/recursion/combination-sum.java) | Medium | backtracking | Yes | same pattern pick not pick just we can pick same element mutiple time  so not inc that time Also handle other cases |
| 2 | [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | [Code](dsa/recursion/combination-sum-iI.java) | Hard | backtracking | Yes | - |
| 3 | [78. Subsets](https://leetcode.com/problems/subsets/description/) | [Code](dsa/recursion/find_Subsets.java) | Medium | backtracking | Yes | subsequence pattern to pick and not pick current element dual recursion call |

### Trees

| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |
|---|---------|---------|-------|---------|---------|-------------|
| 1 | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/description//) | [Code](dsa/Trees/level-order-traversal.java) | Easy | Tree BFS | No | use Queue interate over curr ques size remove elemet &  store every child in queue |
| 2 | [144. Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/description/) | [Code](dsa/Trees/preorder-traversal.java) | Easy | recursion | No | ROOT->LEFT->RIGHT |
| 3 | [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/description/) | [Code](dsa/Trees/invert-binary-tree.java) | Easy | Recursion DFS(PREORDER) | No | Swap left child and right child if current node is not null |
| 4 | [450. Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/description/) | [Code](dsa/Trees/delete-node-bst.java) | Medium | basic Tree | Yes | Leaf Node: Just delete it.  One Child: Replace node with its only child.  Two Children: Replace with inorder predecessor (rightmost of left subtree) or inorder successor (leftmost of right subtree). We’ll use predecessor here. |
| 5 | [701. Insert into a Binary Search Tree](https://leetcode.com/problems/insert-into-a-binary-search-tree/description/) | [Code](dsa/Trees/insert-into-bst.java) | Easy | Simple BST | No | both way recursion & iteration |

